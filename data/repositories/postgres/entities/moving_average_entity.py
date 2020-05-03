from sqlalchemy_utils import IntRangeType
from intervals import IntInterval

from data.repositories.postgres.entities import db
from domain.entities.moving_average import MovingAverage
from domain.entities.candle_duration import CandleDuration


class MovingAverageEntity(db.Model):
    __tablename__ = "moving_averages"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    value = db.Column(db.Float, nullable=False)
    candle_duration_in_seconds = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    time_range = db.Column(IntRangeType, nullable=False)  # Closed left, open right
    first_close_time = db.Column(db.Integer, nullable=False)

    def __init__(self,
                 value: float,
                 candle_duration_in_seconds: int,
                 order: int,
                 time_range: IntInterval):
        self.value = value
        self.candle_duration_in_seconds = candle_duration_in_seconds
        self.order = order
        self.time_range = time_range
        self.first_close_time = time_range.upper - candle_duration_in_seconds * order

    def to_domain(self) -> MovingAverage:
        return MovingAverage(self.value,
                             CandleDuration.from_human_readable(self.candle_duration),
                             self.order,
                             self.time_range.lower,
                             self.time_range.upper,
                             self.id)

    @classmethod
    def from_domain(cls, moving_average: MovingAverage):
        return MovingAverageEntity(moving_average.value,
                                   moving_average.candle_duration.in_seconds(),
                                   moving_average.order,
                                   moving_average.time_range)
