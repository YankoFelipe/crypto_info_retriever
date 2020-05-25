from domain.entities.candle_duration import CandleDuration


class MovingAverageSpec:
    def __init__(self, candle_duration: CandleDuration, order: int, _id: int = None):
        self.candle_duration = candle_duration
        self.order = order
        self.id = _id

    def __eq__(self, other):
        if not isinstance(other, MovingAverageSpec):
            raise NotImplementedError
        return self.candle_duration == other.candle_duration and self.order == other.order

    def as_key(self) -> str:
        return self.candle_duration.value + str(self.order)

    @classmethod
    def from_labels(cls, as_human_readable: str, order: str):
        return MovingAverageSpec(CandleDuration.from_human_readable(as_human_readable), int(order))

    def candle_in_seconds(self) -> int:
        return self.candle_duration.in_seconds()
