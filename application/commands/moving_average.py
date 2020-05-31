from application.repositories import prices_repo, moving_averages_repo
from application.modules.data_checker import DataChecker
from application.modules.moving_average_generator import MovingAverageGenerator
from domain.entities.moving_average_spec import MovingAverageSpec
from domain.entities.candle_duration import CandleDuration


class MovingAverageCommand:
    def __init__(self, order: str, candle_duration: str):
        try:
            self.ma_spec = MovingAverageSpec.from_labels(candle_duration, order)
        except:
            print("The parameter '--order' must be a integer")
            print("The parameter '--candle_duration' must be one of the following")
            [print(e.value) for e in CandleDuration]
            exit(0)

    def do(self):
        has_spec = DataChecker.has_moving_average_spec(self.ma_spec)
        has_moving_averages = DataChecker.has_moving_averages(self.ma_spec)
        has_prices = DataChecker.has_prices()
        if not has_prices:
            print('The "price" table is empty! Go get some using the prices command first. Then come back.')
            exit(0)
        print(f'Generating moving averages of {self.ma_spec.candle_duration.value} candles and order {str(self.ma_spec.order)}')
        if has_moving_averages:
            print('Resuming from where it was left')

        MovingAverageGenerator(prices_repo, moving_averages_repo, self.ma_spec)\
            .fill_table(has_spec=has_spec, is_resuming=has_moving_averages)

        print('Done')
        print('If you want more data to test get more prices. Otherwise prepare the training camp.')
