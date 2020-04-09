from data.streams.trade_stream import TradeStream
from data.repositories.postgres.trade_repository import TradeRepository
from data.repositories.postgres.price_repository import PriceRepository
from domain.entities.price import Price


class HistoricalPriceGenerator:
    time_step_size = 5  # Seconds
    current_time: int
    current_price: Price
    current_trade = None
    previous_trade = None

    def __init__(self):
        self.trade_stream = TradeStream(TradeRepository())
        self.prices_repo = PriceRepository()

    def fill_table(self, is_resuming: bool = False):
        if is_resuming:
            last_time = self.prices_repo.get_last_time()
            self.trade_stream.init_from_last_price_time(last_time - self.time_step_size)
            print('Last price time found')
        self.next()
        self.init_time(self.current_trade.time)
        self.new_price(self.current_trade.price)

        while self.trade_stream.is_alive():
            if self.current_trade.time == self.time() + self.time_step_size:
                self.new_price(self.current_trade.price)
                self.update_time()

            while self.current_trade.time > self.time() + self.time_step_size:
                self.new_price(self.previous_trade.price)
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
        self.prices_repo.save(self.current_price)
