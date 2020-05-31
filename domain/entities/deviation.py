from datetime import datetime, timezone

from domain.entities.deviation_spec import DeviationSpec


class Deviation:
    time: datetime

    def __init__(self,
                 spec: DeviationSpec,
                 time: datetime = None,
                 _id: int = None):
        self.id = _id
        self.spec = spec
        self.time = time

    def set_time_from_stamp(self, time: int):
        self.time = datetime.fromtimestamp(time, timezone.utc)
