from data.streams.abstract_stream import AbstractStream
from data.repositories.postgres.trade_repository import TradeRepository


class TradeStream(AbstractStream):
    _is_alive = True
    id: int = 0

    def __init__(self, trades_repo: TradeRepository):
        self.trades_repo = trades_repo
        self.id = int(self.trades_repo.get_first_id())

    def next(self):
        self.id += 1
        new_trade = self.trades_repo.get(self.id)
        if not bool(new_trade):
            self._is_alive = False
        return new_trade

    def is_alive(self) -> bool:
        return self._is_alive
