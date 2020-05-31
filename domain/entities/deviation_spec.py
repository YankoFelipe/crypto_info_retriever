from domain.entities.moving_average_spec import MovingAverageSpec


class DeviationSpec:
    def __init__(self,
                 ma_spec: MovingAverageSpec,
                 percentage: float,
                 _id: int = None):
        self.id = _id
        self.ma_spec = ma_spec
        self.percentage = percentage

    @classmethod
    def from_labels(cls, order: str, candle_duration: str, percentage: float):  # TODO: think a better name
        ma_spec = MovingAverageSpec.from_labels(candle_duration, order)
        return DeviationSpec(ma_spec, percentage)
