import abc
import pandas as pd


class NewsSourceInterface(abc.ABC):
    ticker: str = None

    def get_ticker(self) -> str:
        return self.ticker

    @abc.abstractmethod
    def get_news(self) -> pd.DataFrame:
        raise NotImplementedError("Needs to be implemented by subclass.")
