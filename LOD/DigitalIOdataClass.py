import pandas as pd
import matplotlib.pyplot as plt
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class DigitalIOdataClass(TimeSeriesDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_DigitalIO.csv'
        self.Direction = {
            'AX0': [], 'AX1': [], 'AX2': [], 'AX3': [],
            'AX4': [], 'AX5': [], 'AX6': [], 'AX7': []
        }
        self.State = {
            'AX0': [], 'AX1': [], 'AX2': [], 'AX3': [],
            'AX4': [], 'AX5': [], 'AX6': [], 'AX7': []
        }

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.Direction['AX0'] = data[:, 1]
        self.Direction['AX1'] = data[:, 2]
        self.Direction['AX2'] = data[:, 3]
        self.Direction['AX3'] = data[:, 4]
        self.Direction['AX4'] = data[:, 5]
        self.Direction['AX5'] = data[:, 6]
        self.Direction['AX6'] = data[:, 7]
        self.Direction['AX7'] = data[:, 8]
        self.State['AX0'] = data[:, 9]
        self.State['AX1'] = data[:, 10]
        self.State['AX2'] = data[:, 11]
        self.State['AX3'] = data[:, 12]
        self.State['AX4'] = data[:, 13]
        self.State['AX5'] = data[:, 14]
        self.State['AX6'] = data[:, 15]
        self.State['AX7'] = data[:, 16]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

    def plot(self):
        if self.NumPackets == 0:
            raise ValueError('No data to plot.')
        else:
            time = range(1, self.NumPackets + 1) if self.Time is None else self.Time
            fig, ax = plt.subplots()
            ax.plot(time, self.State['AX0'], 'r', label='AX0')
            ax.plot(time, self.State['AX1'], 'g', label='AX1')
            ax.plot(time, self.State['AX2'], 'b', label='AX2')
            ax.plot(time, self.State['AX3'], 'k', label='AX3')
            ax.plot(time, self.State['AX4'], ':r', label='AX4')
            ax.plot(time, self.State['AX5'], ':g', label='AX5')
            ax.plot(time, self.State['AX6'], ':b', label='AX6')
            ax.plot(time, self.State['AX7'], ':k', label='AX7')
            ax.set_title('Digital I/O')
            ax.set_xlabel(self.time_axis)
            ax.set_ylabel('State (Binary)')
            ax.legend()
            plt.show()

# 사용 예:
# fileNamePrefix = 'example_prefix'
# digital_io_data = DigitalIOdataClass(fileNamePrefix, SampleRate=1)
# digital_io_data.plot()
