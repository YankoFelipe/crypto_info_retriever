from abc import abstractmethod

from domain.repositories.abstract_repository import AbstractRepository
from domain.entities.moving_average import MovingAverage
from domain.entities.moving_average_spec import MovingAverageSpec


class MovingAverageRepository(AbstractRepository):
    @abstractmethod
    def save(self, moving_average: MovingAverage):
        pass

    @abstractmethod
    def save_spec(self, spec: MovingAverageSpec) -> int:
        pass

    @abstractmethod
    def get_spec_id(self, spec: MovingAverageSpec) -> bool:
        pass

    @abstractmethod
    def has_spec(self, spec: MovingAverageSpec) -> bool:
        pass

    @abstractmethod
    def has_data(self, spec: MovingAverageSpec) -> bool:
        pass

    @abstractmethod
    def get_first_time_of_last_average(self, moving_average_spec: MovingAverageSpec) -> int:
        pass

    @abstractmethod
    def get_initial_time(self, spec: MovingAverageSpec) -> int:
        pass

    @abstractmethod
    def get(self, spec: MovingAverageSpec, time: int) -> MovingAverage:
        pass
