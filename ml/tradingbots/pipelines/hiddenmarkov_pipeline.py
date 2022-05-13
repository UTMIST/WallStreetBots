from backend.settings import BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY
from pipeline import Pipeline
from ..components.hiddenmarkov import DataManager
from ..components.hiddenmarkov import HMM
from ..components.naiveportfoliomanager import NaiveHMMPortfolioUpdate
import datetime
from datetime import timedelta
from ..components.utils import AlpacaFetcher


class HMMPipline(Pipeline):

    def pipeline(self):
        data_fetcher = AlpacaFetcher(BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY)
        buffer = 0.05
        start = (datetime.datetime.now(datetime.timezone.utc) - timedelta(days=1)).isoformat()
        end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        num_hidden_states, covar_type, n_iter = 10, 'full', 100
        NHPU = NaiveHMMPortfolioUpdate(self.portfolio, data_fetcher, DataManager, start, end, HMM, num_hidden_states,
                              covar_type, n_iter, buffer=buffer)
        return NHPU.rebalance()