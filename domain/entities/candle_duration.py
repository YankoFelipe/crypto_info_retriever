import enum

from domain.constants.dt import dt


class CandleDuration(enum.Enum):
    one_minute = '1m'
    three_minutes = '3m'
    five_minutes = '5m'
    fifteen_minutes = '15m'
    thirty_minutes = '30m'
    one_hour = '1h'
    two_hours = '2h'
    six_hours = '6h'
    twelve_hours = '12h'
    one_day = '1d'
    one_week = '1w'
    four_weeks = '4w'

    @staticmethod
    def from_human_readable(label: str):
        if not isinstance(label, str):
            raise Exception("The label must be a string")
        if label == '1m':
            return CandleDuration.one_minute
        elif label == '3m':
            return CandleDuration.three_minutes
        elif label == '5m':
            return CandleDuration.five_minutes
        elif label == '15m':
            return CandleDuration.fifteen_minutes
        elif label == '30m':
            return CandleDuration.thirty_minutes
        elif label == '1h':
            return CandleDuration.one_hour
        elif label == '2h':
            return CandleDuration.two_hours
        elif label == '6h':
            return CandleDuration.six_hours
        elif label == '12h':
            return CandleDuration.twelve_hours
        elif label == '1d':
            return CandleDuration.one_day
        elif label == '1w':
            return CandleDuration.one_week
        elif label == '4w':
            return CandleDuration.four_weeks
        else:
            raise NotImplementedError

    def human_readable(self) -> str:
        return self.value

    def in_seconds(self) -> int:
        if self.value == '1m':
            return 60
        elif self.value == '3m':
            return 180
        elif self.value == '5m':
            return 300
        elif self.value == '15m':
            return 900
        elif self.value == '30m':
            return 1800
        elif self.value == '1h':
            return 3600
        elif self.value == '2h':
            return 7200
        elif self.value == '6h':
            return 21600
        elif self.value == '12h':
            return 43200
        elif self.value == '1d':
            return 86400
        elif self.value == '1w':
            return 86400 * 7
        elif self.value == '4w':
            return 86400 * 28

    def in_steps(self) -> int:
        return int(self.in_seconds() / dt)
