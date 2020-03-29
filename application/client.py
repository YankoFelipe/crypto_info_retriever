from os import getenv
from binance.client import Client

client = Client(getenv("API_KEY"), getenv("SECRET_KEY"))
