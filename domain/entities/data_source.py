import enum


class DataSource(enum.Enum):
    local = 'local'
    remote = 'remote'

    @staticmethod
    def from_str(label):
        if label == 'local':
            return DataSource.local
        elif label == 'remote':
            return DataSource.remote
        else:
            raise NotImplementedError
