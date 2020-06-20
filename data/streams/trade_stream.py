from data.streams.abstract_stream import AbstractStream
from data.repositories.postgres.trade_repository import TradeRepository


class TradeStream(AbstractStream):
    _is_alive = True
    id: int = 0
    current_trade = None

    def __init__(self, trades_repo: TradeRepository):
        self.trades_repo = trades_repo
        self.id = int(self.trades_repo.get_first_id())

    def next(self):
        self.id += 1
        self.current_trade = self.trades_repo.get(self.id)
        if not bool(self.current_trade):
            self._is_alive = False
        return self.current_trade

    def is_alive(self) -> bool:
        return self._is_alive

    def init_from_last_price_time(self, last_price_time: int):
        self.id = self.trades_repo.get_id_at_time(last_price_time)

    def time(self):
        return self.current_trade.time

    def previous_time(self):
        return self.trades_repo.get(self.id-1).time

    def price(self):
        return self.current_trade.price

    def previous_price(self):
        return self.trades_repo.get(self.id-1).price

    def set_id(self, _id: int):
        self.id = _id

    def kill(self):
        self._is_alive = False
