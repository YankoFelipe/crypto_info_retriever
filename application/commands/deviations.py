import numpy

from application.repositories import deviations_repo, moving_averages_repo, prices_repo
from application.modules.data_checker import DataChecker
from application.modules.deviation_genetator import DeviationGenerator
from domain.entities.deviation_spec import DeviationSpec
from domain.entities.candle_duration import CandleDuration


class DeviationsCommand:
    deviation_specs = []

    def __init__(self, order: str, candle_duration: str, start: str, finish: str, step: str):
        try:
            start_float = float(start)
            finish_float = float(finish)
            step_float = float(step)
            for percentage in numpy.arange(start_float, finish_float, step_float):
                spec = DeviationSpec.from_labels(order, candle_duration, percentage)
                self.deviation_specs.append(spec)
        except:
            print("The parameters '--start', '--finish' and '--step' must be a numbers, where step < start < finish")
            print("The parameter '--order' must be a integer")
            print("The parameter '--candle_duration' must be one of the following")
            [print(e.value) for e in CandleDuration]
            exit(0)
        try:
            for spec in self.deviation_specs:
                spec.ma_spec.id = moving_averages_repo.get_spec_id(spec.ma_spec)
        except:
            print('The "moving_average_spec" id is missing for the values provided.')
            exit(0)

    def do(self):
        for spec in self.deviation_specs:
            self.generate_deviations_for_spec(spec)

    def generate_deviations_for_spec(self, deviation_spec: DeviationSpec):
        has_moving_averages = DataChecker.has_moving_averages(deviation_spec.ma_spec)
        if not has_moving_averages:
            print('The "moving_average" values are missing for the spec provided.')
            exit(0)
        has_deviation_spec = DataChecker.has_deviation_spec(deviation_spec)
        has_deviations = DataChecker.has_deviations(deviation_spec)

        self.print_welcome(has_deviations, deviation_spec)

        DeviationGenerator(moving_averages_repo,
                           deviations_repo,
                           prices_repo,
                           deviation_spec)\
            .fill_table(has_spec=has_deviation_spec, is_resuming=has_deviations)
        print('Done')

    @staticmethod
    def print_welcome(has_deviations: bool, deviation_spec: DeviationSpec):
        candle = deviation_spec.ma_spec.candle_duration.value
        order = deviation_spec.ma_spec.order
        percentage = deviation_spec.percentage
        print(f'Generating deviations of {percentage}% compared to the moving average {candle} of order {order}')
        if has_deviations:
            print('Resuming from where it was left')
