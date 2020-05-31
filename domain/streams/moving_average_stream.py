from abc import abstractmethod

from domain.streams.abstract_stream import AbstractStream
from domain.repositories.moving_average_repository import MovingAverageRepository
from domain.entities.moving_average_spec import MovingAverageSpec


class MovingAverageStream(AbstractStream):
    def __init__(self, moving_averages_repo: MovingAverageRepository, moving_average_spec: MovingAverageSpec):
        pass

    @abstractmethod
    def get_current_moving_average(self, time: int) -> float:
        pass

    @abstractmethod
    def set_time(self, time: int):
        pass
