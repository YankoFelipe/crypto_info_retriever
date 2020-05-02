from application.repositories import prices_repo, moving_averages_repo
from application.modules.data_checker import DataChecker
from application.modules.moving_average_generator import MovingAverageGenerator
from domain.entities.candle_duration import CandleDuration


class MovingAverageCommand:
    order: int
    candle_duration: CandleDuration

    def __init__(self, order: str, candle_duration: str):
        try:
            self.order = int(order)
        except:
            print("The parameter '--order' must be a integer")
            exit(0)
        try:
            self.candle_duration = CandleDuration.from_human_readable(candle_duration)
        except Exception as e:
            if isinstance(e, Exception):
                print("Invalid value of parameter '--candle_duration'")
            if isinstance(e, NotImplementedError):
                print("Value of '--candle_duration' not implemented")
            print("Please use one of the following")
            [print(e.value) for e in CandleDuration]
            exit(0)

    def do(self):
        has_moving_averages = DataChecker.has_moving_averages(self.candle_duration.in_seconds(), self.order)
        has_prices = DataChecker.has_prices()
        if not has_prices:
            print('The "price" table is empty! Go get some using the prices command first. Then come back.')
            exit(0)
        print('Generating moving averages of ' + self.candle_duration.value + ' candle and order ' + str(self.order))
        if has_moving_averages:
            print('Resuming from where it was left')
        MovingAverageGenerator(prices_repo, moving_averages_repo, self.candle_duration, self.order)\
            .fill_table(is_resuming=has_prices)
        print('Done')
        print('If you want more data to test get more prices. Otherwise prepare the training camp.')
