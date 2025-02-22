from datetime import datetime
from os import getenv

from application.repositories import trades_repo
from application.client import client
from data.repositories.postgres.entities.trade_entity import TradeEntity


class Retriever:
    @classmethod
    def retrieve_1000_trades(cls, start_id: int):
        trades = client.get_historical_trades(symbol=getenv('SYMBOL'), limit=1000, fromId=start_id)
        trade_entities = [TradeEntity.from_dict(trade) for trade in trades]
        trades_repo.save_trades(trade_entities)

    @classmethod
    def retrieve_trades(cls, start_id: int, end_id: int):
        if end_id < start_id:
            raise Exception("end_id must be greater than start_id")
        current_id = start_id
        tries = 1
        while current_id < end_id:
            try:
                trades = client.get_historical_trades(symbol=getenv('SYMBOL'), limit=1000, fromId=current_id)
                tries = 1
            except:
                if tries > 4:
                    raise Exception("All is lost")
                tries += 1
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("id " + str(current_id) + " failed at " + current_time + " retry " + str(tries))
            else:
                trade_entities = [TradeEntity.from_dict(trade) for trade in trades]
                trades_repo.save_trades(trade_entities)
                current_id += 1000
