from database import StockDB
from database import ListDB
from datetime import datetime, timedelta
import time


def load_to_stock_list(stock: str):
    mystocks = ListDB()
    stock = stock.upper()
    existing_stocks = mystocks.my_list()

    if stock in existing_stocks:
        print(f'{stock} is already on the list.')
        return f'{stock} is already on the list.'
    else:
        mystocks.add_stock(stock)
        print(f'{stock} was added to the list.')
        return f'{stock} was added to the list.'


def load_csv_to_stock_list(csvfile: str):
    import csv

    with open(csvfile, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        [load_to_stock_list(row[0]) for row in reader]

    return "Done"


def load_all_overviews_incomes_targets():
    my_stocks = ListDB()
    stock_list = my_stocks.my_list()
    list_len = len(stock_list)
    i = 1

    for item in stock_list:
        stock = StockDB(item)
        check = stock.check()

        if not check['overview']:
            stock.add_overview()
            print(f'{item} - Added overview')
            print(f'Waiting 12 seconds (API limit - 5 req per min)')
            time.sleep(12)
        else:
            print(f'Overview for {item} is already in the DB')

        if not check['income']:
            stock.add_income()
            print(f'{item} - Added income')
            print(f'Waiting 12 seconds (API limit - 5 req per min)')
            time.sleep(12)
        else:
            print(f'Income for {item} is already in the DB')

        if not check['targets']:
            stock.add_targets()
            print(f'{item} - Added targets')
            print(f'Waiting 12 seconds (API limit - 5 req per min)')
            time.sleep(12)
        else:
            print(f'Targets for {item} is already in the DB')

        print(f'Item {i} of {list_len}')
        i = i + 1

    return 'Done'


def update_prices():
    my_stocks = ListDB()
    stock_list = my_stocks.my_list()
    list_len = len(stock_list)
    if datetime.date(datetime.now()).weekday() in [5, 6]:
        today = datetime.date(datetime.now())
        day_delta = datetime.date(datetime.now()).weekday() - 4
        d = timedelta(days=day_delta)
        today = today - d
        today = today.strftime("%Y-%m-%d")
    else:
        today = datetime.date(datetime.now()).strftime("%Y-%m-%d")
    i = 1

    for item in stock_list:
        stock = StockDB(item)
        check = stock.check()
        timing = stock.check_timing()['prices']

        if timing == today:
            print(f'Price of {item} is already updated')
            pass
        else:
            if not check['prices']:
                stock.add_prices()
                print(f'{item} - Added prices')

            else:
                doc_id = stock.get_prices()[0]['_id']
                stock.delete_price_record(doc_id)
                stock.add_prices()
                print(f'{item} - Added targets')

        print(f'{item} is done')
        print(f'Item {i} of {list_len}')
        time.sleep(30)
        i = i + 1

    return 'Done'


def update_overview():
    my_stocks = ListDB()
    stock_list = my_stocks.my_list()
    list_len = len(stock_list)
    i = 1

    for item in stock_list:
        stock = StockDB(item)
        if stock.check()['overview']:
            record_id = stock.get_overview()[0]['_id']
            stock.delete_overview_record(record_id)
            stock.add_overview()
        else:
            stock.add_overview()

        print(f'Record {i} of {list_len}')
        time.sleep(30)
        i = i + 1

    return "Overview updated"


def update_income():
    my_stocks = ListDB()
    stock_list = my_stocks.my_list()
    list_len = len(stock_list)
    i = 1

    for item in stock_list:
        stock = StockDB(item)
        if stock.check()['income']:
            record_id = stock.get_income()[0]['_id']
            stock.delete_income_record(record_id)
            stock.add_income()
        else:
            stock.add_income()

        print(f'Record {i} of {list_len}')
        time.sleep(30)
        i = i + 1

    return "Income updated"


def update_target():
    my_stocks = ListDB()
    stock_list = my_stocks.my_list()
    list_len = len(stock_list)
    i = 1

    for item in stock_list:
        stock = StockDB(item)
        if stock.check()['targets']:
            record_id = stock.get_targets()[0]['_id']
            stock.delete_target_record(record_id)
            stock.add_targets()
        else:
            stock.add_targets()

        print(f'Record {i} of {list_len}')
        i = i + 1

    return "Targets updated"


if __name__ == '__main__':
    update_prices()
