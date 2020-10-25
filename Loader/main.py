import schedule
import time
from helpers import update_prices
from helpers import update_income
from helpers import update_overview
from helpers import update_target
from datetime import date
import threading


def daily_job():
    print("Starting daily job")
    update_prices()
    update_overview()


def friday_job():
    print("Starting Friday job")
    update_target()


def income_job():
    print("Checking income job")
    if date.today().day != 20:
        print("Nothing to do")
        pass
    else:
        update_income()
        print("Income updated")


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every().day.at("23:45").do(run_threaded, daily_job())
schedule.every().Friday.at("12:00").do(run_threaded, friday_job())
schedule.every().day.at("14:00").do(run_threaded, income_job())


while 1:
    schedule.run_pending()
    time.sleep(200)