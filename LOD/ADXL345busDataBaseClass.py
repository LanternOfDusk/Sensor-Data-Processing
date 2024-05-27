import pandas as pd
import matplotlib.pyplot as plt
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class ADXL345busDataBaseClass(TimeSeriesDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_ADXL345bus.csv'
        self.ADXL345A = {'X': [], 'Y': [], 'Z': []}
        self.ADXL345B = {'X': [], 'Y': [], 'Z': []}
        self.ADXL345C = {'X': [], 'Y': [], 'Z': []}
        self.ADXL345D = {'X': [], 'Y': [], 'Z': []}
        self.AccelerometerUnits = ''

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

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

    def plot(self):
        if self.NumPackets == 0:
            raise ValueError('No data to plot.')
        else:
            time = range(1, self.NumPackets + 1) if self.Time is None else self.Time
            fig, axs = plt.subplots(4, 1, sharex=True, num=self.create_fig_name())

            axs[0].plot(time, self.ADXL345A['X'], 'r', label='X')
            axs[0].plot(time, self.ADXL345A['Y'], 'g', label='Y')
            axs[0].plot(time, self.ADXL345A['Z'], 'b', label='Z')
            axs[0].legend()
            axs[0].set_ylabel(f'Acceleration ({self.AccelerometerUnits})')
            axs[0].set_title('ADXL345 A')

            axs[1].plot(time, self.ADXL345B['X'], 'r', label='X')
            axs[1].plot(time, self.ADXL345B['Y'], 'g', label='Y')
            axs[1].plot(time, self.ADXL345B['Z'], 'b', label='Z')
            axs[1].legend()
            axs[1].set_ylabel(f'Acceleration ({self.AccelerometerUnits})')
            axs[1].set_title('ADXL345 B')

            axs[2].plot(time, self.ADXL345C['X'], 'r', label='X')
            axs[2].plot(time, self.ADXL345C['Y'], 'g', label='Y')
            axs[2].plot(time, self.ADXL345C['Z'], 'b', label='Z')
            axs[2].legend()
            axs[2].set_ylabel(f'Acceleration ({self.AccelerometerUnits})')
            axs[2].set_title('ADXL345 C')

            axs[3].plot(time, self.ADXL345D['X'], 'r', label='X')
            axs[3].plot(time, self.ADXL345D['Y'], 'g', label='Y')
            axs[3].plot(time, self.ADXL345D['Z'], 'b', label='Z')
            axs[3].legend()
            axs[3].set_xlabel(self.time_axis)
            axs[3].set_ylabel(f'Acceleration ({self.AccelerometerUnits})')
            axs[3].set_title('ADXL345 D')

            plt.show()

# 사용 예:
# fileNamePrefix = 'example_prefix'
# adxl345_data = ADXL345busDataBaseClass(fileNamePrefix, SampleRate=1)
# adxl345_data.plot()
