import pandas as pd
from datetime import datetime
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class DateTimeDataClass(TimeSeriesDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_DateTime.csv'
        self.String = []
        self.Vector = []
        self.Serial = []

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        file_name = self.create_file_name(fileNamePrefix)
        data = pd.read_csv(file_name, delimiter=',', header=None, skiprows=1)
        self.Vector = data.iloc[:, 1:7].values.tolist()
        self.String = [datetime(*map(int, row)).strftime('%Y-%m-%d %H:%M:%S') for row in self.Vector]
        self.Serial = [datetime(*map(int, row)).timestamp() for row in self.Vector]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

    def plot(self):
        raise NotImplementedError("This method is unimplemented.")

# 사용 예:
# fileNamePrefix = 'example_prefix'
# datetime_data = DateTimeDataClass(fileNamePrefix, SampleRate=1)
# print(datetime_data.String)
# print(datetime_data.Serial)
