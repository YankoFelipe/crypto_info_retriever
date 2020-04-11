from application.repositories import trades_repo, prices_repo


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
