from data.streams.abstract_stream import AbstractStream
from data.repositories.postgres.price_repository import PriceRepository


class TradeStream(AbstractStream):
    _is_alive = True

    def __init__(self, trades_repo: PriceRepository):
        self.trades_repo = trades_repo
        self.id = self.trades_repo.get_first_id()

    def next(self):
        self.id += 1
        new_price = self.trades_repo.get(self.id)
        if not bool(new_price):
            self._is_alive = False
        return

    def is_alive(self) -> bool:
        return self._is_alive
