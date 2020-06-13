from application.repositories import deviations_repo, moving_averages_repo
from use_cases.histogram_of_deviations_use_case import HistogramOfDeviationsUseCase
from domain.entities.deviation_spec import DeviationSpec
from domain.entities.candle_duration import CandleDuration


class AnalyseDeviationsCommand:
    def __init__(self,
                 order: str,
                 candle_duration: str,
                 percentage: str):
        try:
            percentage_float = float(percentage)
            self.spec = DeviationSpec.from_labels(order, candle_duration, percentage_float)
        except:
            print("The parameter '--percentage' must be a float")
            print("The parameter '--order' must be a integer")
            print("The parameter '--candle_duration' must be one of the following")
            [print(e.value) for e in CandleDuration]
            exit(0)

    def do(self):
        self.spec.ma_spec.id = moving_averages_repo.get_spec_id(self.spec.ma_spec)
        self.spec.id = deviations_repo.get_spec_id(self.spec)
        HistogramOfDeviationsUseCase(deviations_repo).process(self.spec)
