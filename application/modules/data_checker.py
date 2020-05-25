from application.repositories import trades_repo, prices_repo, moving_averages_repo
from domain.entities.moving_average_spec import MovingAverageSpec


class DataChecker:
    @staticmethod
    def check_tables() -> (bool, bool):
        return DataChecker.has_trades(), DataChecker.has_prices()

    @staticmethod
    def has_trades() -> bool:
        return trades_repo.has_data()

    @staticmethod
    def has_prices() -> bool:
        return prices_repo.has_data()

    @staticmethod
    def has_moving_average_spec(spec: MovingAverageSpec) -> bool:
        return moving_averages_repo.has_spec(spec)

    @staticmethod
    def has_moving_averages(spec: MovingAverageSpec) -> bool:
        spec_id = moving_averages_repo.get_spec_id(spec)
        return moving_averages_repo.has_data(spec_id) if bool(spec_id) else False
