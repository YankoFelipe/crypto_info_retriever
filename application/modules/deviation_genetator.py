from os import getenv
from datetime import datetime, timezone

from data.streams.price_stream import PriceStream
from domain.repositories.moving_average_repository import MovingAverageRepository
from domain.repositories.price_repository import PriceRepository
from domain.repositories.deviation_repository import DeviationRepository
from domain.managers.moving_average_manager import MovingAverageManager
from domain.entities.market import Market
from domain.entities.deviation_spec import DeviationSpec
from domain.entities.deviation import Deviation


is_positive = lambda x: x >= 0


class DeviationGenerator:
    def __init__(self,
                 moving_averages_repo: MovingAverageRepository,
                 deviations_repo: DeviationRepository,
                 prices_repo: PriceRepository,
                 deviation_spec: DeviationSpec):
        self.moving_averages_repo = moving_averages_repo
        self.deviations_repo = deviations_repo
        self.deviation_spec = deviation_spec
        # Not sure if this is the best forward time ¯\_(ツ)_/¯
        self.forward_time = 1.5 * deviation_spec.ma_spec.candle_duration.in_seconds()
        self.is_positive_deviation = is_positive(self.deviation_spec.percentage)
        price_stream = PriceStream(prices_repo)
        ma_manager = MovingAverageManager([deviation_spec.ma_spec], moving_averages_repo)
        self.market = Market(price_stream, ma_manager, getenv('SYMBOL'), verbose=True)

    def fill_table(self, has_spec: bool = False, is_resuming: bool = False):
        if has_spec:
            self.deviation_spec.id = self.deviations_repo.get_spec_id(self.deviation_spec)
        else:
            self.deviation_spec.id = self.deviations_repo.save_spec(self.deviation_spec)

        if is_resuming:
            raise NotImplementedError('TODO: Implement deviation resuming')
        else:
            initial_time = self.moving_averages_repo.get_initial_time(self.deviation_spec.ma_spec)
            self.market.set_minimal_time(initial_time)
            self.market.new_price()
            print('Initiating from: ' + str(initial_time))

        print('Ready to fill!')
        while self.market.is_alive():
            if self.is_price_over_tolerance():
                time = datetime.fromtimestamp(self.market.current_time(), timezone.utc)
                new_deviation = Deviation(self.deviation_spec, time)
                self.deviations_repo.save(new_deviation)
                self.market.forward(self.forward_time)
            self.market.new_price()

    def is_price_over_tolerance(self) -> bool:
        moving_average_value = self.market.current_moving_average(self.deviation_spec.ma_spec)
        tolerance = moving_average_value * (1.0 + self.deviation_spec.percentage/100.0)
        price = self.market.current_price.value
        return price > tolerance if self.is_positive_deviation else price < tolerance
