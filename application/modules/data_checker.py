from application.repositories import trades_repo, prices_repo, moving_averages_repo, deviations_repo
from domain.entities.moving_average_spec import MovingAverageSpec
from domain.entities.deviation_spec import DeviationSpec


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
    def has_moving_average_spec(ma_spec: MovingAverageSpec) -> bool:
        return moving_averages_repo.has_spec(ma_spec)

    @staticmethod
    def has_moving_averages(ma_spec: MovingAverageSpec) -> bool:
        ma_spec_id = moving_averages_repo.get_spec_id(ma_spec)
        return moving_averages_repo.has_data_for_spec_id(ma_spec_id) if bool(ma_spec_id) else False

    @staticmethod
    def has_deviation_spec(deviation_spec: DeviationSpec) -> bool:
        return deviations_repo.has_spec(deviation_spec)

    @staticmethod
    def has_deviations(deviation_spec: DeviationSpec) -> bool:
        deviation_spec_id = deviations_repo.get_spec_id(deviation_spec)
        return deviations_repo.has_data(deviation_spec_id) if bool(deviation_spec_id) else False
