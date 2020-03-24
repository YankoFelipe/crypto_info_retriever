from os import getenv
import sched
import time

from binance.client import Client
from average import Average

client = Client(getenv("API_KEY"), getenv("SECRET_KEY"))
s = sched.scheduler(time.time, time.sleep)
symbol = getenv("SYMBOL")
delay = 5  # Seconds


def print_price(sc):
    try:
        print(Average.get_average_first(client, 'BTCUSDT'))
    except:
        print('Client error')
    s.enter(delay, 1, print_price, ('first',))


s.enter(delay, 1, print_price, ('first',))

s.run()
