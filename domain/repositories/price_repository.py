from abc import abstractmethod

from domain.repositories.abstract_repository import AbstractRepository
from domain.entities.price import Price


class PriceRepository(AbstractRepository):
    @abstractmethod
    def save(self, price: Price) -> bool:
        pass

    @abstractmethod
    def save_prices(self, prices: [Price]) -> bool:
        pass

    @abstractmethod
    def get_first_id(self) -> int:
        pass

    @abstractmethod
    def get_first_time(self) -> int:
        pass

    @abstractmethod
    def get_last_time(self) -> int:
        pass

    @abstractmethod
    def get(self, price_id: int) -> Price:
        pass

    @abstractmethod
    def get_chunk(self, from_id: int, chunk_size: int, as_dict: bool = False) -> [Price]:
        pass

    @abstractmethod
    def has_data(self) -> bool:
        pass

    @abstractmethod
    def get_id_at(self, time: int) -> int:
        pass
