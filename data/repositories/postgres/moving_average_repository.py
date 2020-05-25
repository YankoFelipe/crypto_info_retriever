from sqlalchemy.exc import SQLAlchemyError

from data.repositories.postgres.entities import db
from data.repositories.postgres.entities.moving_average_entity import MovingAverageEntity
from data.repositories.postgres.entities.moving_average_spec_entity import MovingAverageSpecEntity
from domain.entities.moving_average import MovingAverage
from domain.entities.moving_average_spec import MovingAverageSpec


class MovingAverageRepository:
    def save(self, moving_average: MovingAverage):
        try:
            ma_entity = MovingAverageEntity.from_domain(moving_average)
            if self.is_already_saved(ma_entity):
                return False
            db.session.add(ma_entity)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise Exception("Problem saving moving average")
        return True

    def save_spec(self, spec: MovingAverageSpec) -> int:
        if self.has_spec(spec):
            return False
        try:
            spec_entity = MovingAverageSpecEntity.from_domain(spec)
            db.session.add(spec_entity)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise Exception("Problem saving moving average spec")
        return spec_entity.id

    def is_already_saved(self, ma_entity: MovingAverageEntity) -> bool:
        saved_ma = db.session.query(MovingAverageEntity)\
            .filter_by(spec_id=ma_entity.spec_id,
                       time_range=ma_entity.time_range)\
            .first()
        return saved_ma is not None

    def get_first_time_of_last_average(self, spec: MovingAverageSpec) -> int:
        ma_entity = db.session.query(MovingAverageEntity)\
            .filter_by(spec_id=spec.id)\
            .order_by(MovingAverageEntity.first_close_time.desc())\
            .first()
        return ma_entity.first_close_time

    def has_spec(self, spec: MovingAverageSpec) -> bool:
        spec_entity = db.session.query(MovingAverageSpecEntity)\
            .filter_by(order=spec.order, candle_in_seconds=spec.candle_in_seconds())\
            .first()
        return spec_entity is not None

    def get_spec_id(self, spec: MovingAverageSpec) -> bool:
        spec_entity = db.session.query(MovingAverageSpecEntity)\
            .filter_by(order=spec.order, candle_in_seconds=spec.candle_in_seconds())\
            .first()
        return spec_entity.id if bool(spec_entity) else None

    def has_data(self, spec_id: int) -> bool:
        ma_entity = db.session.query(MovingAverageEntity)\
            .filter_by(spec_id=spec_id)\
            .first()
        return ma_entity is not None
