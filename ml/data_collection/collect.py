import queue
import feedparser
from typing import Optional, Dict

q = queue.Queue() # queue of processed items ready to be ingested by data pipeline
rss_sources = []  # list of rss sources with their own processing function


def process_rss_feed_entry(entry: feedparser.util.FeedParserDict) -> Dict[str, str]:
    return {"title": entry.title, "summary": entry.summary}


class RssSource:
    url: str
    process_entry: callable
    _newest_id: Optional[str] = None

    def __init__(self, url, process_entry):
        self.url = url
        self.process_entry = process_entry
        self._newest_id = None

    def get_newest_entry(self):
        feed = feedparser.parse(self.url)
        entry = feed['entries'][0]
        if self._newest_id is None or entry['id'] != self._newest_id:
            self._newest_id = entry['id']
            return self.process_entry(entry)
        return None


def wait_for_newest_rss_feed_entry():
    i = 0
    while True:
        newest_rss_item = rss_sources[i].get_newest_entry()
        if newest_rss_item:
            q.put(newest_rss_item)

        i = (i + 1) % len(rss_sources)



urls = [
    'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'https://www.economist.com/united-states/rss.xml',
    'https://www.economist.com/the-americas/rss.xml'
]

if __name__ == "__main__":
    for url in urls:
        rss_sources.append(RssSource(url, process_rss_feed_entry))
    wait_for_newest_rss_feed_entry()
