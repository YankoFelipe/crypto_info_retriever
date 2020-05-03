from queue import Queue

from domain.entities.candle_duration import CandleDuration
from domain.entities.moving_average import MovingAverage
from domain.entities.price import Price


class MovingAverageCalculator:
    def __init__(self, order: int, candle_duration: CandleDuration, initial_time: int):
        self.order = order
        self.candle_duration = candle_duration
        self.q = Queue(order)

        self.next_closing = self.get_first_closing(initial_time)
        self.current_closing = None

    def get_first_closing(self, initial_time: int) -> int:
        mod = initial_time % self.candle_duration.in_seconds()
        return initial_time if mod == 0 else initial_time - mod + self.candle_duration.in_seconds()

    def is_moving_average_available(self) -> bool:
        return self.q.full()

    def current_moving_average_value(self):
        if not self.q.full():
            raise Exception("Incomplete moving average")
        return sum(list(self.q.queue)) / self.order

    def current_moving_average(self):
        return MovingAverage(self.current_moving_average_value(),
                             self.candle_duration,
                             self.order,
                             self.current_closing,
                             self.next_closing)

    def new_closing(self, closing_price: Price):
        if closing_price.time != self.next_closing:
            raise Exception("Invalid closing time")

        if self.q.full():
            self.q.get()
        self.q.put(closing_price.value, block=False)

        self.current_closing = self.next_closing
        self.next_closing += self.candle_duration.in_seconds()

