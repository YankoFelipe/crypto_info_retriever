from os import getenv
import sched
import time

from binance.client import Client

client = Client(getenv("API_KEY"), getenv("SECRET_KEY"))
s = sched.scheduler(time.time, time.sleep)
symbol = getenv("SYMBOL")
delay = 2  # Seconds


def print_price(sc):
    print(client.get_avg_price(symbol=symbol)['price'])
    s.enter(delay, 1, print_price, ('first',))


s.enter(delay, 1, print_price, ('first',))

s.run()
