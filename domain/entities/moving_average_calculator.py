from queue import Queue

from domain.entities.moving_average_spec import MovingAverageSpec
from domain.entities.moving_average import MovingAverage
from domain.entities.price import Price


class MovingAverageCalculator:
    def __init__(self, spec: MovingAverageSpec, initial_time: int):
        self.spec = spec
        self.q = Queue(spec.order)

        self.next_closing = self.get_first_closing(initial_time)
        self.current_closing = None

    def get_first_closing(self, initial_time: int) -> int:
        mod = initial_time % self.spec.candle_in_seconds()
        return initial_time if mod == 0 else initial_time - mod + self.spec.candle_in_seconds()

    def is_moving_average_available(self) -> bool:
        return self.q.full()

    def current_moving_average_value(self):
        if not self.q.full():
            raise Exception("Incomplete moving average")
        return sum(list(self.q.queue)) / self.spec.order

    def current_moving_average(self):
        return MovingAverage(self.current_moving_average_value(),
                             self.spec,
                             self.current_closing,
                             self.next_closing)

    def new_closing(self, closing_price: Price):
        if closing_price.time != self.next_closing:
            raise Exception("Invalid closing time")

        if self.q.full():
            self.q.get()
        self.q.put(closing_price.value, block=False)

        self.current_closing = self.next_closing
        self.next_closing += self.spec.candle_in_seconds()
