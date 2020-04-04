class Trade:
    def __init__(self,
                 _id: int,
                 price: float,
                 qty: float,
                 quote_quantity: float,
                 time: int,
                 is_buyer_maker: bool,
                 is_best_match: bool):
        self.id = _id
        self.price = price
        self.quantity = qty
        self.quote_quantity = quote_quantity
        self.time = time
        self.is_buyer_maker = is_buyer_maker
        self.is_best_match = is_best_match
