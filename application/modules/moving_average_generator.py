from data.streams.price_stream import PriceStream
from data.repositories.postgres.moving_average_repository import MovingAverageRepository
from data.repositories.postgres.price_repository import PriceRepository
from domain.entities.candle_duration import CandleDuration
from domain.entities.moving_average_calculator import MovingAverageCalculator


class MovingAverageGenerator:
    current_time: int
    ma_calculator = None
    price_stream = None
    current_price = None
    saved_averages = []

    def __init__(self,
                 prices_repo: PriceRepository,
                 moving_averages_repo: MovingAverageRepository,
                 candle_duration: CandleDuration,
                 order: int):
        self.prices_repo = prices_repo
        self.moving_averages_repo = moving_averages_repo
        self.candle_duration = candle_duration
        self.order = order

    def fill_table(self, is_resuming: bool = False):
        self.price_stream = PriceStream(self.prices_repo)
        self.price_stream.next()

        if is_resuming:
            print('Preparing to resume')
            self.current_time = self.moving_averages_repo\
                .get_first_time_of_last_average(self.candle_duration, self.order) - self.candle_duration.in_seconds()
            print('Resuming from: ' + str(self.current_time))
        else:
            self.current_time = self.price_stream.time()
            print('Initiating from: ' + str(self.current_time))

        self.ma_calculator = MovingAverageCalculator(self.order,
                                                     self.candle_duration,
                                                     self.current_time)
        print('Ready to fill!')
        while self.price_stream.is_alive():
            if self.price_stream.time() % self.candle_duration.in_seconds() == 0:
                self.ma_calculator.new_closing(self.current_price)
                if self.ma_calculator.is_moving_average_available():
                    new_moving_average = self.ma_calculator.current_moving_average()
                    self.moving_averages_repo.save(new_moving_average)
            self.next()

    def next(self):
        self.current_price = self.price_stream.next()
