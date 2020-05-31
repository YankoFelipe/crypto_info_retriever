from typing import List

from domain.repositories.moving_average_repository import MovingAverageRepository
from domain.entities.moving_average_spec import MovingAverageSpec


class MovingAverageManager:
    moving_averages: dict

    def __init__(self,
                 specs: List[MovingAverageSpec],
                 moving_averages_repo: MovingAverageRepository):
        if not isinstance(specs, list) or len(specs) == 0:
            raise Exception('Not a list of specs')
        self.specs = specs
        self.moving_averages_repo = moving_averages_repo
        self.moving_averages = {}

    def get_current(self, spec: MovingAverageSpec, time: int) -> float:
        if spec not in self.specs:
            raise Exception('Unknown spec')

        saved_ma = self.moving_averages.get(spec.as_key())

        if not saved_ma or time not in saved_ma.time_range:
            new_moving_average = self.moving_averages_repo.get(spec, time)
            self.moving_averages[spec.as_key()] = new_moving_average
            return new_moving_average.value if bool(new_moving_average) else None
        else:
            return saved_ma.value

    def get_minimal_times(self) -> [int]:
        return [self.moving_averages_repo.get_initial_time(spec) for spec in self.specs]
