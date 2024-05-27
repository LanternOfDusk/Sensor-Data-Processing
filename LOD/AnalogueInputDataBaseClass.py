import pandas as pd
import matplotlib.pyplot as plt
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class AnalogueInputDataBaseClass(TimeSeriesDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_AnalogueInput.csv'
        self.AX0 = []
        self.AX1 = []
        self.AX2 = []
        self.AX3 = []
        self.AX4 = []
        self.AX5 = []
        self.AX6 = []
        self.AX7 = []
        self.ADCunits = ''

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

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

    def plot(self):
        if self.NumPackets == 0:
            raise ValueError('No data to plot.')
        else:
            time = range(1, self.NumPackets + 1) if self.Time is None else self.Time
            fig, ax = plt.subplots()
            ax.plot(time, self.AX0, 'r', label='AX0')
            ax.plot(time, self.AX1, 'g', label='AX1')
            ax.plot(time, self.AX2, 'b', label='AX2')
            ax.plot(time, self.AX3, 'k', label='AX3')
            ax.plot(time, self.AX4, ':r', label='AX4')
            ax.plot(time, self.AX5, ':g', label='AX5')
            ax.plot(time, self.AX6, ':b', label='AX6')
            ax.plot(time, self.AX7, ':k', label='AX7')
            ax.set_xlabel(self.time_axis)
            ax.set_ylabel(f'Voltage ({self.ADCunits})')
            ax.set_title('Analogue Input')
            ax.legend()
            plt.show()

# 사용 예:
# fileNamePrefix = 'example_prefix'
# analogue_input_data = AnalogueInputDataBaseClass(fileNamePrefix, SampleRate=1)
# analogue_input_data.plot()
