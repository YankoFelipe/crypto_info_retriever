from application.repositories import deviations_repo, moving_averages_repo
from use_cases.histogram_of_deviations_use_case import HistogramOfDeviationsUseCase
from domain.entities.deviation_spec import DeviationSpec
from domain.entities.candle_duration import CandleDuration


class AnalyseAllDeviationsCommand:
    def __init__(self):
        print("Getting histograms for all stored deviations")

    def do(self):
        specs = deviations_repo.get_all()
        for spec in specs:
            HistogramOfDeviationsUseCase(deviations_repo).process(spec)
