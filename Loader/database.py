from cloudant.client import Cloudant
from cloudant.query import Query
from environs import Env
from av import Stock
from target import targets

env = Env()
env.read_env()


class StockDB:
    def __init__(self, ticker):
        self.url = env("CLOUDANT_URL")
        self.readkey = env("CLOUDANT_KEY_READ")
        self.readuser = env("CLOUDANT_USERNAME_READ")
        self.readpass = env("CLOUDANT_PASS_READ")
        self.writekey = env("CLOUDANT_KEY_WRITE")
        self.writeuser = env("CLOUDANT_USERNAME_WRITE")
        self.writepass = env("CLOUDANT_PASS_WRITE")
        self.ticker = ticker

    def add_overview(self):
        client = Cloudant(self.writeuser,
                          self.writepass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-overview']
        document = Stock(self.ticker).load_overview()
        my_database.create_document(document)

        return f'Overview for {self.ticker} added successfully'

    def add_income(self):
        client = Cloudant(self.writeuser,
                          self.writepass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-income']
        document = Stock(self.ticker).load_income()
        my_database.create_document(document)

        return f'Income for {self.ticker} added successfully'

    def add_prices(self):
        client = Cloudant(self.writeuser,
                          self.writepass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-prices']
        document = Stock(self.ticker).load_price()
        document['symbol'] = self.ticker
        my_database.create_document(document)

        return f'Prices for {self.ticker} added successfully'

    def add_targets(self):
        client = Cloudant(self.writeuser,
                          self.writepass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-targets']
        document = targets(self.ticker)
        document['symbol'] = self.ticker
        my_database.create_document(document)

        return f'Targets for {self.ticker} added successfully'

    def get_overview(self):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-overview']
        query = Query(my_database, selector={'Symbol': self.ticker})
        data = [doc for doc in query()['docs']]

        return data

    def get_income(self):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-income']
        query = Query(my_database, selector={'symbol': self.ticker})
        data = [doc for doc in query()['docs']]

        return data

    def get_prices(self):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-prices']
        query = Query(my_database, selector={'symbol': self.ticker})
        data = [doc for doc in query()['docs']]

        return data

    def get_targets(self):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-targets']
        query = Query(my_database, selector={'symbol': self.ticker})
        data = [doc for doc in query()['docs']]

        return data

    def delete_price_record(self, doc_id):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-prices']
        # First retrieve the document
        my_document = my_database[doc_id]
        # Delete the document
        my_document.delete()
        return "Document deleted"

    def delete_overview_record(self, doc_id):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-overview']
        # First retrieve the document
        my_document = my_database[doc_id]
        # Delete the document
        my_document.delete()
        return "Document deleted"

    def delete_income_record(self, doc_id):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-income']
        # First retrieve the document
        my_document = my_database[doc_id]
        # Delete the document
        my_document.delete()
        return "Document deleted"

    def delete_target_record(self, doc_id):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stock-targets']
        # First retrieve the document
        my_document = my_database[doc_id]
        # Delete the document
        my_document.delete()
        return "Document deleted"

    def check(self):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        income_db = client['stock-income']
        overview_db = client['stock-overview']
        prices_db = client['stock-prices']
        target_db = client['stock-targets']
        incomequery = Query(income_db, selector={'symbol': self.ticker})
        overviewquery = Query(overview_db, selector={'Symbol': self.ticker})
        pricequery = Query(prices_db, selector={'symbol': self.ticker})
        targetquery = Query(target_db, selector={'symbol': self.ticker})
        try:
            income = self.ticker in incomequery()['docs'][0]['symbol']
        except IndexError:
            income = False

        try:
            overview = self.ticker in overviewquery()['docs'][0]['Symbol']
        except IndexError:
            overview = False

        try:
            prices = self.ticker in pricequery()['docs'][0]['symbol']
        except IndexError:
            prices = False

        try:
            stock_targets = self.ticker in targetquery()['docs'][0]['symbol']
        except IndexError:
            stock_targets = False

        return {'ticker': self.ticker,
                'income': income,
                'overview': overview,
                'targets': stock_targets,
                'prices': prices}

    def check_timing(self):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        prices_db = client['stock-prices']
        pricequery = Query(prices_db, selector={'symbol': self.ticker})

        try:
            prices = pricequery()['docs'][0]['Meta Data']['3. Last Refreshed']
        except IndexError:
            prices = False

        return {'ticker': self.ticker,
                'prices': prices}


class ListDB:
    def __init__(self):
        self.url = env("CLOUDANT_URL")
        self.readkey = env("CLOUDANT_KEY_READ")
        self.readuser = env("CLOUDANT_USERNAME_READ")
        self.readpass = env("CLOUDANT_PASS_READ")
        self.writekey = env("CLOUDANT_KEY_WRITE")
        self.writeuser = env("CLOUDANT_USERNAME_WRITE")
        self.writepass = env("CLOUDANT_PASS_WRITE")

    def add_stock(self, ticker):
        client = Cloudant(self.writeuser,
                          self.writepass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stocks-2-track']
        document = {'ticker': ticker}
        my_database.create_document(document)

        return f'Stock {ticker} added to the list'

    def my_list(self):
        client = Cloudant(self.readuser,
                          self.readpass,
                          url=self.url,
                          connect=True, auto_renew=True)
        my_database = client['stocks-2-track']
        data = [document['ticker'] for document in my_database]

        return data


if __name__ == '__main__':
    IBM = StockDB('MA')
    print(IBM.get_overview())
