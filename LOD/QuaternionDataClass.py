import pandas as pd
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class QuaternionDataClass(TimeSeriesDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_Quaternion.csv'
        self.Quaternion = []

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.Quaternion = data[:, 1:5]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

    def plot(self):
        raise NotImplementedError("This method is unimplemented.")

# 사용 예:
# fileNamePrefix = 'example_prefix'
# quaternion_data = QuaternionDataClass(fileNamePrefix, SampleRate=1)
# quaternion_data.plot()
