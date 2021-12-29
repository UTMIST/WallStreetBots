from collect_news import NewsSource
from collect_finviz_articles import FinVizArticles
import fire


def main(input_file: str = "stock_list.txt"):
    # read every line from input file
    stock_tickers = []
    for line in open(input_file):
        stock_tickers.append(line.strip())

    news_sources = []
    for stock in stock_tickers:
        news_sources.append(NewsSource(stock))
        news_sources.append(FinVizArticles(stock))

    for news_source in news_sources:
        news_source.get_news().to_csv(news_source.__class__.__name__ + news_source.ticker + '.csv')


if __name__ == "__main__":
    fire.Fire(main)
