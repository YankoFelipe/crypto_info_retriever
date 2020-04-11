from data.streams.abstract_stream import AbstractStream
from data.repositories.postgres.trade_repository import TradeRepository

def optional_map(optional_arg, f):
    if optional_arg is None:
        return None
    return f(optional_arg)

class TradeStream(AbstractStream):
    _is_alive = True
    id: int = 0

    def __init__(self, trades_repo: TradeRepository):
        self.trades_repo = trades_repo
        self.id = optional_map(self.trades_repo.get_first_id(), int) or 0

    def next(self):
        self.id += 1
        new_trade = self.trades_repo.get(self.id)
        if not bool(new_trade):
            self._is_alive = False
        return new_trade

    def is_alive(self) -> bool:
        return self._is_alive

    def init_from_last_price_time(self, last_price_time: int):
        self.id = self.trades_repo.get_id_at_time(last_price_time)
