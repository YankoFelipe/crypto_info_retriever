from data.repositories.postgres.entities import db
from domain.entities.price import Price
from domain.constants.dt import dt


class PriceEntity(db.Model):
    __tablename__ = "prices"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.Integer, nullable=False)

    def __init__(self, value: float, time: int):
        self.value = value
        if time % dt > 0:
            raise Exception('Invalid time!')
        self.time = time

    @classmethod
    def from_domain(cls, price: Price):
        return PriceEntity(price.value, price.time)

    @classmethod
    def from_dict(cls, adict: dict):
        return PriceEntity(adict.get("price"), adict.get("time"))

    def to_domain(self) -> Price:
        return Price(self.value, self.time)
