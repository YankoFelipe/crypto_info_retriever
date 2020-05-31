from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql import func

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

    def save_prices(self, prices: [Price]) -> bool:
        if self.is_already_saved(prices[-1].time):
            return True  # skip this chunk
        is_valid_chunk = False
        try:
            for price in prices:
                if not is_valid_chunk and self.is_already_saved(price.time):
                    continue
                else:
                    is_valid_chunk = True
                price_entity = PriceEntity.from_domain(price)
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
        return db.session.query(func.min(PriceEntity.id)).one()[0]

    def get_first_time(self) -> int:
        return db.session.query(func.min(PriceEntity.time)).one()[0]

    def get_last_time(self) -> int:
        return db.session.query(func.max(PriceEntity.time)).one()[0]

    def get(self, price_id: int) -> Price:
        return db.session.query(PriceEntity).get(price_id).to_domain()

    def get_chunk(self, from_id: int, chunk_size: int, as_dict: bool = False) -> [Price]:
        entities = db.session.query(PriceEntity)\
            .filter(PriceEntity.id.between(from_id, from_id+chunk_size))\
            .limit(chunk_size)\
            .all()
        ret = {}
        if as_dict:
            for item in entities:
                ret[item.id] = item.to_domain()
        else:
            ret = [item.to_domain() for item in entities]
        return ret

    def has_data(self) -> bool:
        return db.session.query(PriceEntity).first() is not None

    def get_id_at(self, time: int) -> int:
        return db.session.query(PriceEntity).filter_by(time=time).first().id
