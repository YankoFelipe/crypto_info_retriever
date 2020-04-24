from application.modules.data_checker import DataChecker
from application.modules.historical_price_generator import HistoricalPriceGenerator
from domain.entities.data_source import DataSource


class PricesCommand:
    def __init__(self, source: str):
        self.source = DataSource.from_str(source)

    def do(self):
        has_trades, has_prices = DataChecker.check_tables()
        if (self.source is DataSource.local) and not has_trades:
            print('The "trades" table is empty! Go get some using the trades command first. Then come back.')
            exit(0)
        print('Generating historical prices')
        if has_prices:
            print('Resuming from where it was left')
        HistoricalPriceGenerator(self.source).fill_table(is_resuming=has_prices)
        print('Done')
        print('If you want more data to test get more trades. Otherwise prepare the training camp')
