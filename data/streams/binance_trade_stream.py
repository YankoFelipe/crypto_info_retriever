from data.streams.abstract_stream import AbstractStream
from data.repositories.binance.binance_repository import BinanceRepository
from domain.constants.epoch_id import epoch_id


class BinanceTradeStream(AbstractStream):
    _is_alive = True
    id: int = 0
    current_trades = {}
    current_trade = None
    previous_trade = None

    def __init__(self, binance_repo: BinanceRepository, use_domain_trades: bool = True):
        self.binance_repo = binance_repo
        self.use_domain_trades = use_domain_trades
        self.id = epoch_id
        self.update_dict()

    def next(self):
        self.id += 1
        self.previous_trade = self.current_trade
        self.current_trade = self.current_trades.get(self.id)
        if not self.current_trade:
            print('Getting 1000 more trades from ' + str(self.id))
            self.update_dict()
            self.current_trade = self.current_trades.get(self.id)
            if not self.current_trade:
                self._is_alive = False
        return self.current_trade

    def is_alive(self) -> bool:
        return self._is_alive

    def update_dict(self):
        self.current_trades = self.binance_repo.thousand_trades_from_id(self.id, self.use_domain_trades)

    def set_id(self, new_id: int):
        self.id = new_id - new_id % 1000
        self._is_alive = True
        self.update_dict()

    def time(self):
        return self.current_trade.time if self.use_domain_trades else int(self.current_trade['time']/1000)

    def previous_time(self):
        return self.previous_trade.time if self.use_domain_trades else int(self.previous_trade['time']/1000)

    def price(self):
        return self.current_trade.price if self.use_domain_trades else self.current_trade['price']

    def previous_price(self):
        return self.previous_trade.price if self.use_domain_trades else self.previous_trade['price']
