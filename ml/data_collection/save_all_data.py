from collect_news import NewsSource
from collect_finviz_articles import FinVizArticles

if __name__ == "__main__":
    news_sources = []
    news_sources.append(NewsSource("AAPL", num_rows=10))
    news_sources.append(NewsSource("MSFT", num_rows=10))
    news_sources.append(NewsSource("GOOG", num_rows=10))
    news_sources.append(FinVizArticles('amzn'))

    for news_source in news_sources:
        news_source.get_news().to_csv(news_source.__class__.__name__ + news_source.ticker + '.csv')
