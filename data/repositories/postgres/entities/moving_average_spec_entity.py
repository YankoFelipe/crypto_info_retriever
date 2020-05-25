from sqlalchemy.orm import relationship

from data.repositories.postgres.entities import db
from domain.entities.moving_average_spec import MovingAverageSpec
from domain.entities.candle_duration import CandleDuration


class MovingAverageSpecEntity(db.Model):
    __tablename__ = "moving_average_specs"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    candle_in_human_readable = db.Column(db.String(4), nullable=False)
    candle_in_seconds = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)

    moving_averages = relationship("MovingAverageEntity", back_populates='spec', cascade="delete")

    def __init__(self,
                 candle_in_human_readable: str,
                 candle_in_seconds: int,
                 order: int):
        self.candle_in_human_readable = candle_in_human_readable
        self.candle_in_seconds = candle_in_seconds
        self.order = order

    def to_domain(self) -> MovingAverageSpec:
        return MovingAverageSpec(CandleDuration.from_human_readable(self.candle_in_human_readable),
                                 self.order,
                                 self.id)

    @classmethod
    def from_domain(cls, moving_average_spec: MovingAverageSpec):
        return MovingAverageSpecEntity(moving_average_spec.candle_duration.value,
                                       moving_average_spec.candle_in_seconds(),
                                       moving_average_spec.order)
