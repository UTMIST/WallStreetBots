import requests
import json
import pandas as pd


API_TOKEN = "OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX"
URL = "https://eodhistoricaldata.com/api/news?api_token=OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX&s=AAPL.US&offset=0&limit=10"


def get_raw_data(ticker, limit, date_from=None, date_to=None):
    if date_from is None:
        url = "https://eodhistoricaldata.com/api/news?api_token={}&s={}&offset=0&limit={}".format(API_TOKEN, ticker, limit)
    else:
        url = "https://eodhistoricaldata.com/api/news?api_token={}&s={}&from={}&to={}&offset=0&limit={}".format(API_TOKEN, ticker, date_from, date_to, limit)
    response = requests.get(url)
    content = response.content
    parsed = json.loads(content)

    return parsed

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

def main():
    parsed = get_raw_data("AAPL.US", 10)
    df = to_dataframe(parsed)
    print(df)


if __name__ == "__main__":
    main()
    




