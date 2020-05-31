from sqlalchemy.orm import relationship

from data.repositories.postgres.entities import db
from domain.entities.deviation_spec import DeviationSpec
from domain.entities.moving_average_spec import MovingAverageSpec


class DeviationSpecEntity(db.Model):
    __tablename__ = "deviation_specs"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ma_spec_id = db.Column(db.Integer, db.ForeignKey("moving_average_specs.id"), nullable=False)
    percentage = db.Column(db.Float, nullable=False)

    deviations = relationship("DeviationEntity", back_populates='deviation_spec', cascade="delete")
    ma_spec = relationship("MovingAverageSpecEntity")

    def __init__(self, ma_spec: MovingAverageSpec, percentage: float):
        if not ma_spec.id:
            raise Exception('Deviation spec entity constructor without MA spec ID')
        self.ma_spec_id = ma_spec.id
        self.percentage = percentage

    def to_domain(self) -> DeviationSpec:
        return DeviationSpec(self.ma_spec.to_domain(),
                             self.percentage,
                             self.id)

    @classmethod
    def from_domain(cls, deviation_spec: DeviationSpec):
        return DeviationSpecEntity(deviation_spec.ma_spec,
                                   deviation_spec.percentage)
