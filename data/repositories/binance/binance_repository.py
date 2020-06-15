from datetime import datetime
from intervals import IntInterval

from domain.entities.trade import Trade


class BinanceRepository:
    def __init__(self, client, symbol: str):
        self.client = client
        self.symbol = symbol

    def thousand_trades_from_id(self, from_id: int, to_domain: bool = True) -> dict:
        adict = {}
        trades_response = None
        tries = 1
        while not trades_response:
            try:
                trades_response = self.client.get_historical_trades(symbol=self.symbol, limit=1000, fromId=from_id)
            except:
                tries += 1
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("id " + str(from_id) + " failed at " + current_time + " retry " + str(tries))
            else:
                tries = 1
        for trade in trades_response:
            _id = trade['id']
            adict[_id] = Trade.from_dict(trade) if to_domain else trade
        return adict

    def price_now(self):
        try:
            depth = self.client.get_order_book(symbol=self.symbol)
            first_bid = float(depth['bids'][0][0])
            first_ask = float(depth['asks'][0][0])
            return (first_bid + first_ask)/2
        except:
            print('get_average_first: Client error')

    def get_id_at_time(self, time: int) -> int:
        # TODO: Improve this with a better search
        if datetime.fromtimestamp(time) > datetime.now():
            raise Exception("Must be a time in the past")
        candidate_id = 0
        next_candidate_id = 0
        current_trades = self.thousand_trades_from_id(candidate_id)
        if time < current_trades[0].time:
            raise Exception("Must be a time after the beginning of the exchange")
        time_covered = self.time_covered_by_trades(current_trades)
        while time > time_covered.upper:
            candidate_id = next_candidate_id
            next_candidate_id += 1000000
            trades = self.thousand_trades_from_id(next_candidate_id)
            time_covered = self.time_covered_by_trades(trades)
        return candidate_id

    @staticmethod
    def time_covered_by_trades(trades: [Trade]) -> IntInterval:
        ids = list(trades.keys())
        return IntInterval.closed(trades[ids[0]].time, trades[ids[-1]].time)
