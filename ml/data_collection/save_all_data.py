import fire
from collect_finviz_articles import FinVizArticles
from collect_news import NewsSource
import pandas as pd


def main(input_file: str = "stock_list.txt"):
    # read every line from input file
    stock_tickers = []
    for line in open(input_file):
        stock_tickers.append(line.strip())

    # collect news data
    news_sources = []
    for stock in stock_tickers:
        news_sources.append(NewsSource(stock))
        news_sources.append(FinVizArticles(stock))

    all_data = []
    for news_source in news_sources:
        # news_source.get_news().to_csv(news_source.__class__.__name__ + news_source.ticker + '.csv', index=False)
        df = news_source.get_news()
        df['ticker'] = news_source.ticker
        all_data.append(df)

    combined_df = pd.concat(all_data)
    combined_df.to_csv('all_data.csv', index=False)


if __name__ == "__main__":
    fire.Fire(main)
