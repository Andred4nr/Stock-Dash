import requests
from environs import Env

env = Env()
env.read_env()


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.key = env("AVKEY")
        self.base = 'https://www.alphavantage.co/query'

    def load_income(self):
        payload = {'function': 'INCOME_STATEMENT',
                   'symbol': self.ticker,
                   'apikey': self.key}
        r = requests.get(self.base, params=payload)
        item = r.json()

        return item

    def load_overview(self):
        payload = {'function': 'OVERVIEW',
                   'symbol': self.ticker,
                   'apikey': self.key}
        r = requests.get(self.base, params=payload)
        item = r.json()

        return item

    def load_price(self):
        payload = {'function': 'TIME_SERIES_DAILY',
                   'symbol': self.ticker,
                   'outputsize': 'full',
                   'apikey': self.key}
        r = requests.get(self.base, params=payload)
        item = r.json()

        return item


if __name__ == '__main__':
    print(Stock('IBM').load_price())
