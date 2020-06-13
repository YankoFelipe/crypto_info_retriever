from sqlalchemy.exc import SQLAlchemyError

from data.repositories.postgres.entities import db
from data.repositories.postgres.entities.deviation_spec_entity import DeviationSpecEntity
from data.repositories.postgres.entities.deviation_entity import DeviationEntity
from data.repositories.postgres.helpers.helpers import deviations_to_domain
from domain.utils.transform_or_none import transform_or_none
from domain.repositories.deviation_repository import DeviationRepository as IDeviationRepository
from domain.entities.deviation_spec import DeviationSpec
from domain.entities.deviation import Deviation


class DeviationRepository(IDeviationRepository):
    def save(self, deviation: Deviation):
        try:
            deviation_entity = DeviationEntity.from_domain(deviation)
            if self.is_already_saved(deviation_entity):
                return False
            db.session.add(deviation_entity)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise Exception("Problem saving deviation")
        return True

    def save_spec(self, spec: DeviationSpec):
        if self.has_spec(spec):
            return False
        try:
            spec_entity = DeviationSpecEntity.from_domain(spec)
            db.session.add(spec_entity)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise Exception("Problem saving deviation spec")
        return spec_entity.id

    def has_spec(self, spec: DeviationSpec) -> bool:
        spec_entity = db.session.query(DeviationSpecEntity)\
            .filter_by(ma_spec_id=spec.ma_spec.id, percentage=spec.percentage)\
            .first()
        return spec_entity is not None

    def get_spec_id(self, spec: DeviationSpec) -> bool:
        spec_entity = db.session.query(DeviationSpecEntity)\
            .filter_by(ma_spec_id=spec.ma_spec.id, percentage=spec.percentage)\
            .first()
        return spec_entity.id if bool(spec_entity) else None

    def has_data(self, spec_id: int) -> bool:
        deviation_entity = db.session.query(DeviationEntity)\
            .filter_by(deviation_spec_id=spec_id)\
            .first()
        return deviation_entity is not None

    def is_already_saved(self, deviation_entity: DeviationEntity) -> bool:
        saved_deviation = db.session.query(DeviationEntity)\
            .filter_by(deviation_spec_id=deviation_entity.deviation_spec_id,
                       time=deviation_entity.time)\
            .first()
        return saved_deviation is not None

    def get_by_spec(self, spec: [DeviationSpec]) -> [Deviation]:
        spec_entity = db.session.query(DeviationSpecEntity).get(spec.id)
        return transform_or_none(deviations_to_domain, spec_entity)

    def get_all(self) -> [DeviationSpec]:
        return [spec.to_domain() for spec in db.session.query(DeviationSpecEntity).all()]
