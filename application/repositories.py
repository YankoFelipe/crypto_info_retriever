from os import getenv

from application.client import client
from data.repositories.postgres.trade_repository import TradeRepository
from data.repositories.postgres.price_repository import PriceRepository
from data.repositories.postgres.moving_average_repository import MovingAverageRepository
from data.repositories.binance.binance_repository import BinanceRepository

trades_repo = TradeRepository()
prices_repo = PriceRepository()
moving_averages_repo = MovingAverageRepository()
binance_repo = BinanceRepository(client, getenv('SYMBOL'))
