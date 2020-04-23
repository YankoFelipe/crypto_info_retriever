from data.streams.abstract_stream import AbstractStream
from data.repositories.postgres.price_repository import PriceRepository
from domain.entities.price import Price
from domain.constants.dt import dt


class PriceStream(AbstractStream):
    _is_alive = True
    id = 1
    chunk_size = 250000

    previous_buffer = {}
    current_buffer = {}

    current_prices = {}
    current_price = None
    previous_price = None

    def __init__(self, prices_repo: PriceRepository):
        self.prices_repo = prices_repo
        self.update_dict()

    def next(self) -> Price:
        self.id += 1
        self.previous_price = self.current_price
        self.current_price = self.current_prices.get(self.id)
        if not self.current_price:
            print('Getting ' + str(self.chunk_size) + ' more trades from ' + str(self.id))
            self.update_dict()
            self.current_price = self.current_prices.get(self.id)
            if not self.current_price:
                self._is_alive = False
        return self.current_price

    def is_alive(self) -> bool:
        return self._is_alive

    def is_dt_ok(self):
        return (self.current_price.time - self.previous_price.time) == dt

    def update_dict(self):
        self.previous_buffer = self.current_buffer
        self.current_buffer = self.prices_repo.get_chunk(self.id, self.chunk_size, as_dict=True)
        self.current_prices = self.current_buffer.copy()
        self.current_prices.update(self.previous_buffer)

    def time(self) -> int:
        return self.current_price.time

    def previous_time(self) -> int:
        return self.previous_price.time

    def value(self) -> float:
        return self.current_price.value

    def previous_value(self) -> float:
        return self.previous_price.value

    def past_value(self, offset: int) -> float:
        return self.current_prices[self.id - offset].value

    def current_id(self):
        return self.id
