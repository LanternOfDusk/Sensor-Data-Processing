import pandas as pd
from ADXL345busDataBaseClass import ADXL345busDataBaseClass  # 이미 구현된 ADXL345busDataBaseClass를 import합니다.

class CalADXL345busDataClass(ADXL345busDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__(fileNamePrefix, **kwargs)
        self.FileNameAppendage = '_CalADXL345bus.csv'

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

        # Set protected parent class variables
        self.AccelerometerUnits = 'g'

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.ADXL345A['X'] = data[:, 1]
        self.ADXL345A['Y'] = data[:, 2]
        self.ADXL345A['Z'] = data[:, 3]
        self.ADXL345B['X'] = data[:, 4]
        self.ADXL345B['Y'] = data[:, 5]
        self.ADXL345B['Z'] = data[:, 6]
        self.ADXL345C['X'] = data[:, 7]
        self.ADXL345C['Y'] = data[:, 8]
        self.ADXL345C['Z'] = data[:, 9]
        self.ADXL345D['X'] = data[:, 10]
        self.ADXL345D['Y'] = data[:, 11]
        self.ADXL345D['Z'] = data[:, 12]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

# 사용 예:
# fileNamePrefix = 'example_prefix'
# cal_adxl345_data = CalADXL345busDataClass(fileNamePrefix, SampleRate=1)
# cal_adxl345_data.plot()
