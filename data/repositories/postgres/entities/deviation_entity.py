from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, func
from datetime import datetime

from data.repositories.postgres.entities import db
from domain.entities.deviation import Deviation
from domain.entities.deviation_spec import DeviationSpec


class DeviationEntity(db.Model):
    __tablename__ = "deviations"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    deviation_spec_id = db.Column(db.Integer, db.ForeignKey("deviation_specs.id"), nullable=False)
    time = db.Column(DateTime(timezone=True), server_default=func.now())

    deviation_spec = relationship("DeviationSpecEntity")

    def __init__(self,
                 deviation_spec: DeviationSpec,
                 time: datetime):
        if not deviation_spec.id:
            raise Exception('Deviation entity constructor without spec ID')
        self.deviation_spec_id = deviation_spec.id
        self.time = time

    def to_domain(self) -> Deviation:
        return Deviation(self.deviation_spec.to_domain(),
                         self.time,
                         self.id)

    @classmethod
    def from_domain(cls, deviation: Deviation):
        return DeviationEntity(deviation.spec,
                               deviation.time)
