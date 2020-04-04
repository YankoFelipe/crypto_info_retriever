from data.repositories.postgres.entities import db
from domain.entities.trade import Trade


class TradeEntity(db.Model):
    first_id = 35000000
    __tablename__ = "trades"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quote_quantity = db.Column(db.Float, nullable=False)
    time = db.Column(db.Integer, nullable=False)  # Unix epoch in ms
    is_buyer_maker = db.Column(db.Boolean, nullable=False)
    is_best_match = db.Column(db.Boolean, nullable=False)

    def __init__(self,
                 _id: int,
                 price: str,
                 qty: str,
                 quote_quantity: str,
                 time: int,
                 is_buyer_maker: bool,
                 is_best_match: bool):
        self.id = _id
        self.price = float(price)
        self.quantity = float(qty)
        self.quote_quantity = float(quote_quantity)
        self.time = int(time/1000)
        self.is_buyer_maker = is_buyer_maker
        self.is_best_match = is_best_match

    @classmethod
    def from_dict(cls, adict: dict):
        return TradeEntity(adict.get("id"),
                           adict.get("price"),
                           adict.get("qty"),
                           adict.get("quoteQty"),
                           adict.get("time"),
                           adict.get("isBuyerMaker"),
                           adict.get("isBestMatch"))

    def to_domain(self) -> Trade:
        return Trade(self.id,
                     self.price,
                     self.quantity,
                     self.quote_quantity,
                     self.time,
                     self.is_buyer_maker,
                     self.is_best_match)