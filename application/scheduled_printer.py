from os import getenv
import sched
import time

from average import Average
from application.client import client

s = sched.scheduler(time.time, time.sleep)
symbol = getenv("SYMBOL")
delay = 1  # Seconds


def print_price(sc):
    try:
        trades = client.get_historical_trades(symbol="BTCUSDT")
        print(Average.get_average_first(client, 'BTCUSDT'))
    except:
        print('Client error')
    s.enter(delay, 1, print_price, ('first',))


s.enter(delay, 1, print_price, ('first',))

s.run()

# About trades
# get_historical_trades ID 280000000 maps to 2020-03-26T10:31:32+00:00
# get_historical_trades ID  40000000 maps to 2018-05-01T13:12:55+00:00
