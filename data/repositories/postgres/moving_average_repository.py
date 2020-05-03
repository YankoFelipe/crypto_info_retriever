from sqlalchemy.exc import SQLAlchemyError

from data.repositories.postgres.entities import db
from data.repositories.postgres.entities.moving_average_entity import MovingAverageEntity
from domain.entities.moving_average import MovingAverage
from domain.entities.candle_duration import CandleDuration


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

    def is_already_saved(self, ma_entity: MovingAverageEntity) -> bool:
        saved_ma = db.session.query(MovingAverageEntity)\
            .filter_by(order=ma_entity.order,
                       candle_duration_in_seconds=ma_entity.candle_duration_in_seconds,
                       time_range=ma_entity.time_range)\
            .first()
        return saved_ma is not None

    def has_data(self, candle_duration: int, order: int) -> bool:
        ma_entity = db.session.query(MovingAverageEntity)\
            .filter_by(order=order,
                       candle_duration_in_seconds=candle_duration)\
            .first()
        return ma_entity is not None

    def get_first_time_of_last_average(self, candle_duration: CandleDuration, order: int) -> int:
        ma_entity = db.session.query(MovingAverageEntity)\
            .filter_by(order=order,
                       candle_duration_in_seconds=candle_duration.in_seconds())\
            .order_by(MovingAverageEntity.first_close_time.desc())\
            .first()
        return ma_entity.first_close_time
