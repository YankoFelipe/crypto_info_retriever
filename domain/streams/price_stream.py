from abc import abstractmethod

from domain.entities.price import Price
from domain.streams.abstract_stream import AbstractStream
from domain.repositories.price_repository import PriceRepository


class PriceStream(AbstractStream):
    def __init__(self, prices_repo: PriceRepository, verbose: bool = False):
        pass

    @abstractmethod
    def new_price(self) -> Price:
        pass

    @abstractmethod
    def set_time(self, time: int):
        pass
