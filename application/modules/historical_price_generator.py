from application.repositories import binance_repo
from data.streams.binance_trade_stream import BinanceTradeStream
from data.streams.trade_stream import TradeStream
from data.repositories.postgres.trade_repository import TradeRepository
from data.repositories.postgres.price_repository import PriceRepository
from domain.entities.price import Price
from domain.entities.data_source import DataSource
from domain.constants.dt import dt


class HistoricalPriceGenerator:
    time_step_size = dt
    current_time: int
    current_price: Price
    current_trade = None
    previous_trade = None
    prices_to_save = []

    def __init__(self, source: DataSource):
        if source is DataSource.remote:
            self.trade_stream = BinanceTradeStream(binance_repo, use_domain_trades=False)
        else:
            self.trade_stream = TradeStream(TradeRepository())
        self.prices_repo = PriceRepository()

    def fill_table(self, is_resuming: bool = False):
        if is_resuming:
            print('Preparing to resume')
            last_time = self.prices_repo.get_last_time()
            print('Last time found')
            last_id = binance_repo.get_id_at_time(last_time)
            print('Last id found')
            self.trade_stream.set_id(last_id - last_id % 1000)
        print('Ready to fill!')
        self.next()
        self.init_time(self.trade_stream.time())

        while self.trade_stream.is_alive():
            if self.trade_stream.time() == self.time() + self.time_step_size:
                self.new_price(self.trade_stream.price())
                self.update_time()

            while self.trade_stream.time() > self.time() + self.time_step_size:
                self.new_price(self.trade_stream.previous_price())
                self.update_time()
            self.next()

    def next(self):
        self.previous_trade = self.current_trade
        self.current_trade = self.trade_stream.next()

    def time(self) -> int:
        return self.current_time

    def init_time(self, trade_first_time: int):
        self.current_time = trade_first_time - trade_first_time % self.time_step_size

    def update_time(self):
        self.current_time += self.time_step_size

    def new_price(self, new_price_value: float):
        self.current_price = Price(new_price_value, self.time())
        self.prices_to_save.append(self.current_price)
        if len(self.prices_to_save) == 100:
            self.prices_repo.save_prices(self.prices_to_save)
            self.prices_to_save.clear()
