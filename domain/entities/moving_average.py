from intervals import IntInterval

from domain.entities.candle_duration import CandleDuration


class MovingAverage:
    def __init__(self,
                 value: float,
                 candle_duration: CandleDuration,
                 order: int,
                 time_lower: int,
                 time_upper: int,
                 _id: int = None):
        self.id = _id
        self.value = value
        self.candle_duration = candle_duration
        self.order = order
        if time_lower % candle_duration.in_seconds() > 0:
            raise Exception("Invalid lower interval")
        if time_upper % candle_duration.in_seconds() > 0:
            raise Exception("Invalid upper interval")
        if time_upper - time_lower != candle_duration.in_seconds():
            raise Exception("Invalid covers more than one period")
        self.time_range = IntInterval.closed_open(time_lower, time_upper)

    def __str__(self):
        return f"value: {self.value}\ncandle duration: {self.candle_duration.value}\norder: {self.order}\nlower: {self.time_range.lower}\nupper: {self.time_range.upper}\n-"
