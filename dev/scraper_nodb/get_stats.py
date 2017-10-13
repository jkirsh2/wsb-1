# take submission and standardize
# data points ticker, weight, sentiment

from match_tickers import SymbolFinder
import datetime

def unix_to_string(s, format):
    return datetime.datetime.fromtimestamp(s).strftime(format)

class Post:

    def __init__(self, submission):
        self.submission = submission
        self.date = unix_to_string(submission.created, '%Y-%m-%d')
        self.create_text()

    def create_text(self):
        self.text = self.submission.title + self.submission.selftext

    def calculate_ticker(self, ticker_list, dollar_sign=False):
        finder = SymbolFinder(ticker_list, dollar_sign)
        self.ticker = finder.get_primary_ticker(self.text)

    def calculate_sentiment(self):
        self.sentiment = 1

    def calculate_exposure(self):
        self.exposure = self.submission.ups + 2*self.submission.num_comments

    def get_stats(self, ticker_list, dollar_sign=False):
        self.calculate_ticker(ticker_list, dollar_sign)
        self.calculate_sentiment()
        self.calculate_exposure()

