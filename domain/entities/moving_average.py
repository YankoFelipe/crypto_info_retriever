from intervals import IntInterval

from domain.entities.moving_average_spec import MovingAverageSpec


class MovingAverage:
    def __init__(self,
                 value: float,
                 spec: MovingAverageSpec,
                 time_lower: int,
                 time_upper: int,
                 _id: int = None):
        self.id = _id
        self.value = value
        self.spec = spec
        if time_lower % spec.candle_in_seconds() > 0:
            raise Exception(f"Invalid lower interval {time_lower}")
        if time_upper % spec.candle_in_seconds() > 0:
            raise Exception(f"Invalid upper interval {time_upper}")
        if time_upper - time_lower != spec.candle_in_seconds():
            raise Exception(f"Invalid, {time_lower} and {time_upper} cover more than one period")
        self.time_range = IntInterval.closed_open(time_lower, time_upper)

    def __str__(self):
        return f"value: {self.value}\ncandle duration: {self.spec.candle_duration.value}\norder: {self.spec.order}\nlower: {self.time_range.lower}\nupper: {self.time_range.upper}\n-"
