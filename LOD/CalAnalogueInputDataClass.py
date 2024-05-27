import pandas as pd
from AnalogueInputDataBaseClass import AnalogueInputDataBaseClass  # 이미 구현된 AnalogueInputDataBaseClass를 import합니다.

class CalAnalogueInputDataClass(AnalogueInputDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__(fileNamePrefix, **kwargs)
        self.FileNameAppendage = '_CalAnalogueInput.csv'

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

        # Set protected parent class variables
        self.ADCunits = 'V'

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.AX0 = data[:, 1]
        self.AX1 = data[:, 2]
        self.AX2 = data[:, 3]
        self.AX3 = data[:, 4]
        self.AX4 = data[:, 5]
        self.AX5 = data[:, 6]
        self.AX6 = data[:, 7]
        self.AX7 = data[:, 8]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

# 사용 예:
# fileNamePrefix = 'example_prefix'
# cal_analogue_input_data = CalAnalogueInputDataClass(fileNamePrefix, SampleRate=1)
# cal_analogue_input_data.plot()
