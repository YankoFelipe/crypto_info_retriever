class Price:
    def __init__(self, value: float, time: int):
        self.value = value
        self.time = time

    def __str__(self):
        return f"value: {self.value}\ntime: {self.time}\n-"
