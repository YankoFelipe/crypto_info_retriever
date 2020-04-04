from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from domain.entities.price import Price
from data.repositories.postgres.entities.price_entity import PriceEntity
from data.repositories.postgres.entities import db


class PriceRepository:
    def save(self, price: Price) -> bool:
        try:
            price_entity = PriceEntity.from_domain(price)
            if self.is_already_saved(price.time):
                return True
            db.session.add(price_entity)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise Exception("Problem saving price")
        return True

    @classmethod
    def is_already_saved(cls, time: int):
        try:
            db.session.query(PriceEntity).filter_by(time=time).one()
        except MultipleResultsFound:
            raise Exception("More than one group with the id")
        except NoResultFound:
            return False
        return True

    def get_first_id(self) -> int:
        raise NotImplementedError

    def get(self, price_id: int) -> Price:
        raise db.session.query(PriceEntity).get(price_id).to_domain()
