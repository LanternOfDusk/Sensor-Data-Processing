import pandas as pd
from BatteryAndThermometerDataBaseClass import BatteryAndThermometerDataBaseClass  # 이미 구현된 BatteryAndThermometerDataBaseClass를 import합니다.

class RawBatteryAndThermometerDataClass(BatteryAndThermometerDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_RawBattAndTherm.csv'
        
        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

        # Set protected parent class variables
        self.ThermometerUnits = 'lsb'
        self.BatteryUnits = 'lsb'

    def import_data(self, fileNamePrefix):
        file_name = self.create_file_name(fileNamePrefix)
        data = pd.read_csv(file_name, header=None)
        self.Battery = data.iloc[:, 1].tolist()
        self.Thermometer = data.iloc[:, 2].tolist()
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

# 사용 예:
# fileNamePrefix = 'example_prefix'
# raw_data = RawBatteryAndThermometerDataClass(fileNamePrefix, SampleRate=1)
# raw_data.plot()
