class ExtremeDeltas:
    def __init__(self):
        self.absolute = 0
        self.absolute_id = 0
        self.percentage = 0.0
        self.percentage_id = 0

    def compare_absolute(self, candidate_absolute: float, current_id: int):
        if candidate_absolute > self.absolute:
            self.absolute = candidate_absolute
            self.absolute_id = current_id

    def compare_percentages(self, candidate_percentage: float, current_id: int):
        if candidate_percentage > self.percentage:
            self.percentage = candidate_percentage
            self.percentage_id = current_id
