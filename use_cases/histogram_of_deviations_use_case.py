import os
from interfaces import use_case as uc
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

from domain.entities.deviation_spec import DeviationSpec
from domain.repositories.deviation_repository import DeviationRepository
from domain.constants.forward_time_factor import forward_time_factor
from domain.constants.dt import dt


class HistogramOfDeviationsUseCase(uc.UseCase):
    shortest_wait: timedelta
    longest_wait: timedelta
    forward_time: timedelta
    number_of_unique_days: int
    is_not_forward_time = None

    def __init__(self, deviations_repo: DeviationRepository):
        self.deviations_repo = deviations_repo

    def process(self, spec: DeviationSpec):
        dir_name = spec.ma_spec.as_key()
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        self.forward_time = timedelta(seconds=(forward_time_factor * spec.ma_spec.candle_duration.in_seconds() + dt))
        self.is_not_forward_time = lambda x: x != self.forward_time
        deviations = self.deviations_repo.get_by_spec(spec)
        dates = [deviation.time for deviation in deviations]
        waits = self.differences(dates)
        self.number_of_unique_days = self.get_number_of_days_unique(dates)
        self.shortest_wait = min(list(filter(self.is_not_forward_time, waits)))
        self.longest_wait = max(waits)
        self.weekly_histogram(dates, spec)
        self.monthly_histogram(dates, spec)

    def monthly_histogram(self, dates: [datetime], spec: DeviationSpec):
        number_of_months = self.months_between_dates(dates[-1], dates[0])
        ma_key = spec.ma_spec.as_key()
        percentage = str(spec.percentage)
        histogram_name = f'{ma_key}/months_{percentage}.png'
        title = f'Times per month that the price went beyond the moving average {ma_key} in {percentage} percentage'
        self.save_histogram(dates, number_of_months, histogram_name, 'Year-Month', title)

    def weekly_histogram(self, dates: [datetime], spec: DeviationSpec):
        number_of_weeks = self.weeks_between_dates(dates[0], dates[-1])
        ma_key = spec.ma_spec.as_key()
        percentage = str(spec.percentage)
        histogram_name = f'{ma_key}/weeks_{percentage}.png'
        title = f'Times per week that the price went beyond the moving average {ma_key} in {percentage} percentage'
        self.save_histogram(dates, number_of_weeks, histogram_name, 'Week', title)

    def save_histogram(self,
                       data: [],
                       bins: int,
                       file_name: str,
                       x_label: str,
                       title: str):
        plt.figure(figsize=(12, 6))
        n, bins, patches = plt.hist(data, bins=bins, rwidth=0.8)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel('Number of deviations')
        plt.text(data[0], int(max(n)*0.9), f'Longest wait: {self.longest_wait}')
        plt.text(data[0], int(max(n)*0.6), f'Shortest wait: {self.shortest_wait}')
        plt.text(data[0], int(max(n)*0.3), f'Number of days with deviations: {self.number_of_unique_days}')
        plt.savefig(file_name)
        plt.close()

    def weeks_between_dates(self, start: datetime, finish: datetime) -> int:
        return int(self.days_between_dates(start, finish) // 7)

    def days_between_dates(self, start: datetime, finish: datetime) -> int:
        return abs(finish - start).days

    def months_between_dates(self, start: datetime, finish: datetime) -> int:
        return abs((finish.year - start.year) * 12 + finish.month - start.month)

    def differences(self, a_list: []) -> []:
        return [y - x for x, y in zip(a_list, a_list[1:])]

    def get_number_of_days_unique(self, dates: [datetime]) -> int:
        unique_dates = set()
        [unique_dates.add(d.date()) for d in dates]
        return len(unique_dates)
