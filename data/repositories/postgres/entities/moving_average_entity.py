from sqlalchemy.orm import relationship
from sqlalchemy_utils import IntRangeType
from intervals import IntInterval

from data.repositories.postgres.entities import db
from domain.entities.moving_average import MovingAverage
from domain.entities.moving_average_spec import MovingAverageSpec


class MovingAverageEntity(db.Model):
    __tablename__ = "moving_averages"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    value = db.Column(db.Float, nullable=False)
    spec_id = db.Column(db.Integer, db.ForeignKey("moving_average_specs.id"), nullable=False)
    time_range = db.Column(IntRangeType, nullable=False)  # Closed left, open right
    first_close_time = db.Column(db.Integer, nullable=False)

    spec = relationship("MovingAverageSpecEntity")

    def __init__(self,
                 value: float,
                 spec: MovingAverageSpec,
                 time_range: IntInterval):
        self.value = value
        if not spec.id:
            raise Exception('MA entity constructor without spec ID')
        self.spec_id = spec.id
        self.time_range = time_range
        self.first_close_time = time_range.upper - spec.candle_in_seconds() * spec.order

    def to_domain(self) -> MovingAverage:
        return MovingAverage(self.value,
                             self.spec.to_domain(),
                             self.time_range.lower,
                             self.time_range.upper,
                             self.id)

    @classmethod
    def from_domain(cls, moving_average: MovingAverage):
        return MovingAverageEntity(moving_average.value,
                                   moving_average.spec,
                                   moving_average.time_range)
