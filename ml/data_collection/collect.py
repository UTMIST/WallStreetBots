import queue
import threading
import time
import feedparser

q = queue.Queue()

def wait_for_newest_rss_feed_entry(url):
    feed = feedparser.parse(url)
    newest_entry_id = None
    while True:
        entries = feed['entries']
        if len(entries) > 0 and newest_entry_id != entries[0]['id']:
            newest_entry_id = entries[0]['id']
            print(newest_entry_id)
            q.put(newest_entry_id)
        else:
            time.sleep(5)
            print("waiting")


urls = [
    'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'https://www.economist.com/united-states/rss.xml',
    'https://www.economist.com/the-americas/rss.xml'
]

if __name__ == "__main__":
    for url in urls:
        t = threading.Thread(target=wait_for_newest_rss_feed_entry, args=(url,))
        t.start()
    while True:
        if not q.empty():
            print("getting from queue")
            print(q.get())
