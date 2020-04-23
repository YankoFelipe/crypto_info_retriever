from tabulate import tabulate

from application.repositories import prices_repo
from data.streams.price_stream import PriceStream
from domain.entities.variation_annotator import VariationAnnotator


class CheckPricesTableCommand:
    chunk_size = 100000
    current_price = None
    previous_price = None
    biggest_rise = 0
    biggest_fall = 0
    annotator_steps = [(1, '5s'),
                       (6, '30s'),
                       (12, '1m'),
                       (24, '2m'),
                       (60, '5m'),
                       (120, '10m'),
                       (240, '20m'),
                       (360, '30m'),
                       (720, '1h'),
                       (1440, '2h'),
                       (2880, '4h'),
                       (5760, '8h'),
                       (8640, '12h'),
                       (17280, '1d'),
                       (120960, '7d'),
                       (241920, '14d')]

    def __init__(self):
        self.price_stream = PriceStream(prices_repo)
        self.annotators = [VariationAnnotator(*steps, self.price_stream) for steps in self.annotator_steps]

    def do(self):
        print('Price table check start!')
        self.next()
        self.next()

        while self.price_stream.is_alive():  # and self.price_stream.current_id() < 100000:
            if not self.price_stream.is_dt_ok():
                raise Exception('Error in table at ' + str(self.price_stream.current_id()))
            for annotator in self.annotators:
                annotator.new_step(self.price_stream.value(),
                                   self.price_stream.current_id())
            self.next()

        print('Price table check finish!')
        self.report_annotators()

    def next(self):
        self.previous_price = self.current_price
        self.current_price = self.price_stream.next()

    def report_annotators(self):
        table = []

        for annotator in self.annotators:
            table.append([annotator.number_of_steps,
                          annotator.readable_steps,
                          round(annotator.rise.absolute, 2),
                          round(annotator.rise.percentage, 2),
                          round(annotator.fall.absolute, 2),
                          round(annotator.fall.percentage, 2)])
        headers = ["Slots", "time", "abs rise", "% rise", "abs fall", "% fall"]
        print(tabulate(table, headers=headers))
