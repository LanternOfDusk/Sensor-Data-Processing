import pandas as pd
import matplotlib.pyplot as plt
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class EulerAnglesDataClass(TimeSeriesDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_EulerAngles.csv'
        self.Phi = []
        self.Theta = []
        self.Psi = []

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.Phi = data[:, 1]
        self.Theta = data[:, 2]
        self.Psi = data[:, 3]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

    def plot(self):
        if self.NumPackets == 0:
            raise ValueError('No data to plot.')
        else:
            time = range(1, self.NumPackets + 1) if self.Time is None else self.Time
            fig, ax = plt.subplots()
            ax.plot(time, self.Phi, 'r', label='Phi (φ)')
            ax.plot(time, self.Theta, 'g', label='Theta (θ)')
            ax.plot(time, self.Psi, 'b', label='Psi (ψ)')
            ax.set_title('Euler angles')
            ax.set_xlabel(self.time_axis)
            ax.set_ylabel('Angle (degrees)')
            ax.legend()
            plt.show()

# 사용 예:
# fileNamePrefix = 'example_prefix'
# euler_angles_data = EulerAnglesDataClass(fileNamePrefix, SampleRate=1)
# euler_angles_data.plot()
