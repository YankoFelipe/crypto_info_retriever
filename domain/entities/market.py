from domain.entities.price import Price
from domain.entities.moving_average_spec import MovingAverageSpec
from domain.streams.price_stream import PriceStream
from domain.managers.moving_average_manager import MovingAverageManager


class Market:
    current_price: Price
    last_price: Price
    _is_alive: bool

    def __init__(self,
                 prices_stream: PriceStream,
                 moving_average_manager: MovingAverageManager,
                 symbol: str,
                 verbose: bool = False):
        self.prices_stream = prices_stream
        self.moving_average_manager = moving_average_manager
        self.symbol = symbol
        self.verbose = verbose
        self._is_alive = True
        if self.verbose:
            print(f"Initiating market of {self.symbol}")

    def new_price(self) -> Price:
        new_price = self.prices_stream.new_price()
        if not new_price:
            self._is_alive = False
            self.last_price = self.current_price
        self.current_price = new_price
        return self.current_price

    def current_exchange_price(self) -> float:
        return self.current_price.value

    def current_time(self) -> int:
        return self.current_price.time

    def current_moving_average(self, moving_average_spec: MovingAverageSpec) -> float:
        current_ma = self.moving_average_manager.get_current(moving_average_spec, self.current_time())
        if not current_ma:
            self._is_alive = False
        return current_ma

    def is_alive(self):
        return self._is_alive

    def set_minimal_time(self, time: int):
        self.prices_stream.set_time(time)

    def forward(self, seconds: int):
        time_after_forward = self.current_time() + seconds
        while self.current_time() < time_after_forward:
            self.new_price()
