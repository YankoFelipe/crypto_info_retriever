from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql import func

from domain.entities.trade import Trade
from data.repositories.postgres.entities.trade_entity import TradeEntity
from data.repositories.postgres.entities import db


class TradeRepository:
    def save_trades(self, trades: [TradeEntity]) -> bool:
        try:
            for trade in trades:
                if self.is_already_saved(trade.id):
                    continue
                db.session.add(trade)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise Exception("Problem saving trades")
        return True

    @classmethod
    def is_already_saved(cls, trade_id):
        try:
            db.session.query(TradeEntity).filter_by(id=trade_id).one()
        except MultipleResultsFound:
            raise Exception("More than one group with the id")
        except NoResultFound:
            return False
        return True

    def get_first_id(self) -> int:
        return db.session.query(func.min(TradeEntity.id)).one()[0]

    def get(self, trade_id: int) -> Trade:
        return db.session.query(TradeEntity).get(trade_id).to_domain()
