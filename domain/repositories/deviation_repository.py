from abc import abstractmethod

from domain.repositories.abstract_repository import AbstractRepository
from domain.entities.deviation_spec import DeviationSpec
from domain.entities.deviation import Deviation


class DeviationRepository(AbstractRepository):
    @abstractmethod
    def save(self, deviation: Deviation):
        pass

    @abstractmethod
    def save_spec(self, spec: DeviationSpec):
        pass

    @abstractmethod
    def has_spec(self, deviation_spec: DeviationSpec) -> bool:
        pass

    @abstractmethod
    def get_spec_id(self, spec: DeviationSpec) -> bool:
        pass

    @abstractmethod
    def has_data(self, spec_id: int) -> bool:
        pass
