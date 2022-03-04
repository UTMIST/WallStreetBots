import json

import pandas as pd
import requests

from interface import NewsSourceInterface


class NewsSource(NewsSourceInterface):
    API_TOKEN = "OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX"

    def __init__(self, ticker: str, num_rows: int = 10):
        self.ticker = ticker
        self.num_rows = num_rows

    def get_raw_data(self, date_from=None, date_to=None):
        if date_from is None:
            url = "https://eodhistoricaldata.com/api/news?api_token={}&s={}&offset=0&limit={}" \
                .format(self.API_TOKEN, self.ticker, self.num_rows)
        else:
            url = "https://eodhistoricaldata.com/api/news?api_token={}&s={}&from={}&to={}&offset=0&limit={}". \
                format(self.API_TOKEN, self.ticker, date_from, date_to, self.num_rows)
        response = requests.get(url)
        content = response.content
        try:
            parsed = json.loads(content)
        except json.decoder.JSONDecodeError:
            parsed = {}

        return parsed

    @staticmethod
    def to_dataframe(parsed):
        d = {"date": [], "title": [], "content": [], "symbols": [], "tags": []}
        for i in range(len(parsed)):
            d["date"].append(parsed[i]["date"])
            d["title"].append(parsed[i]["title"])
            d["content"].append(parsed[i]["content"])
            d["symbols"].append(parsed[i]["symbols"])
            d["tags"].append(parsed[i]["tags"])
        df = pd.DataFrame.from_dict(d)

        return df

    def get_news(self):
        parsed = self.get_raw_data()
        df = self.to_dataframe(parsed)
        df.drop(["content", "symbols", "tags"], axis=1, inplace=True)
        return df


def main():
    news_collector = NewsSource("AAPL", num_rows=10)
    df = news_collector.get_news()
    print(df)


if __name__ == "__main__":
    main()
