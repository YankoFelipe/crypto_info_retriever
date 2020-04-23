from domain.entities.extreme_deltas import ExtremeDeltas
from data.streams.price_stream import PriceStream


class VariationAnnotator:

    def __init__(self, number_of_steps: int, human_readable_steps: str, price_stream: PriceStream):
        if not isinstance(number_of_steps, int) or not isinstance(human_readable_steps, str):
            raise Exception('Bad parameter in VariationAnnotator ' + human_readable_steps)
        if number_of_steps > price_stream.chunk_size:
            raise Exception('The buffer of the stream is too small, please increase price_stream.chunk_size')
        self.number_of_steps = number_of_steps
        self.readable_steps = human_readable_steps
        self.price_stream = price_stream
        self.rise = ExtremeDeltas()
        self.fall = ExtremeDeltas()
        self.previous = None

    def new_step(self, current: float, current_step: int):
        if not self.previous:
            self.previous = current

        if current_step > self.number_of_steps + 2:
            self.previous = self.price_stream.past_value(self.number_of_steps)
            self.check_variation(current, current_step)

    def check_variation(self, current: float, current_id: int):
        absolute_delta = abs(current - self.previous)
        percentage_delta = absolute_delta/self.previous * 100

        if current > self.previous:
            self.rise.compare_absolute(absolute_delta, current_id)
            self.rise.compare_percentages(percentage_delta, current_id)

        else:
            self.fall.compare_absolute(absolute_delta, current_id)
            self.fall.compare_percentages(percentage_delta, current_id)
