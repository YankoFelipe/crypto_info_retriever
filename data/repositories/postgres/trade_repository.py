from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql import func

from domain.entities.trade import Trade
from domain.constants.dt import dt
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

    def get_id_at_time(self, time: int) -> int:
        candidate_entity = None
        last_trade_in_table = db.session.query(TradeEntity).order_by(TradeEntity.id.desc()).first()
        if time > last_trade_in_table.time:
            return last_trade_in_table.id - last_trade_in_table.id % 1000
        while not candidate_entity:
            candidate_entity = db.session.query(TradeEntity).filter(TradeEntity.time == time).first()
            if not candidate_entity:
                time -= dt
        return candidate_entity.id

    def get(self, trade_id: int) -> Trade:
        return db.session.query(TradeEntity).get(trade_id).to_domain()

    def get_chunk(self, from_id: int, chunk_size: int) -> dict:
        trade_entities = db.session.query(TradeEntity)\
            .filter(TradeEntity.id.between(from_id, from_id + chunk_size))\
            .all()
        trades_dict = {}
        for trade in trade_entities:
            trades_dict[trade.id] = trade.to_domain()
        return trades_dict

    def has_data(self) -> bool:
        return db.session.query(TradeEntity).first() is not None
