import statistics

from binance.client import Client


class Average:

    @classmethod
    def get_average_api(cls, client: Client, symbol: str) -> float:
        try:
            avg_api = client.get_avg_price(symbol=symbol)['price']
            return float(avg_api)
        except:
            print('get_average_api: Client error')

    @classmethod
    def get_average_book(cls, client: Client, symbol: str) -> float:
        try:
            depth = client.get_order_book(symbol=symbol)
            bids = [float(bid[0]) for bid in depth['bids']]
            asks = [float(ask[0]) for ask in depth['asks']]
            return statistics.mean(bids + asks)
        except:
            print('get_average_book: Client error')

    @classmethod
    def get_average_first(cls, client: Client, symbol: str) -> float:
        try:
            depth = client.get_order_book(symbol=symbol)
            first_bid = float(depth['bids'][0][0])
            first_ask = float(depth['asks'][0][0])
            return (first_bid + first_ask)/2
        except:
            print('get_average_first: Client error')
