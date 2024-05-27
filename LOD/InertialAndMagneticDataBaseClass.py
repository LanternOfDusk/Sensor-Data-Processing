import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class InertialAndMagneticDataBaseClass(TimeSeriesDataBaseClass):
    def __init__(self):
        super().__init__()
        self.Gyroscope = {'X': [], 'Y': [], 'Z': []}
        self.Accelerometer = {'X': [], 'Y': [], 'Z': []}
        self.Magnetometer = {'X': [], 'Y': [], 'Z': []}
        self.GyroscopeUnits = ''
        self.AccelerometerUnits = ''
        self.MagnetometerUnits = ''

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.Gyroscope['X'] = data[:, 1]
        self.Gyroscope['Y'] = data[:, 2]
        self.Gyroscope['Z'] = data[:, 3]
        self.Accelerometer['X'] = data[:, 4]
        self.Accelerometer['Y'] = data[:, 5]
        self.Accelerometer['Z'] = data[:, 6]
        self.Magnetometer['X'] = data[:, 7]
        self.Magnetometer['Y'] = data[:, 8]
        self.Magnetometer['Z'] = data[:, 9]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

    def plot(self):
        if self.NumPackets == 0:
            raise ValueError('No data to plot.')
        else:
            time = np.arange(1, self.NumPackets + 1) if self.Time is None else self.Time
            fig, axs = plt.subplots(3, 1, sharex=True, num=self.create_fig_name())

            axs[0].plot(time, self.Gyroscope['X'], 'r', label='X')
            axs[0].plot(time, self.Gyroscope['Y'], 'g', label='Y')
            axs[0].plot(time, self.Gyroscope['Z'], 'b', label='Z')
            axs[0].legend()
            axs[0].set_xlabel(self.time_axis)
            axs[0].set_ylabel(f'Angular rate ({self.GyroscopeUnits})')
            axs[0].set_title('Gyroscope')

            axs[1].plot(time, self.Accelerometer['X'], 'r', label='X')
            axs[1].plot(time, self.Accelerometer['Y'], 'g', label='Y')
            axs[1].plot(time, self.Accelerometer['Z'], 'b', label='Z')
            axs[1].legend()
            axs[1].set_xlabel(self.time_axis)
            axs[1].set_ylabel(f'Acceleration ({self.AccelerometerUnits})')
            axs[1].set_title('Accelerometer')

            axs[2].plot(time, self.Magnetometer['X'], 'r', label='X')
            axs[2].plot(time, self.Magnetometer['Y'], 'g', label='Y')
            axs[2].plot(time, self.Magnetometer['Z'], 'b', label='Z')
            axs[2].legend()
            axs[2].set_xlabel(self.time_axis)
            axs[2].set_ylabel(f'Flux ({self.MagnetometerUnits})')
            axs[2].set_title('Magnetometer')

            plt.show()

# 사용 예:
# class DerivedInertialAndMagneticClass(InertialAndMagneticDataBaseClass):
#     def __init__(self, fileNamePrefix, sampleRate):
#         super().__init__()
#         self.FileNameAppendage = '_example.csv'
#         self.sample_rate = sampleRate
#         self.import_data(fileNamePrefix)
#         self.GyroscopeUnits = 'deg/s'
#         self.AccelerometerUnits = 'm/s^2'
#         self.MagnetometerUnits = 'uT'
#
# derived_instance = DerivedInertialAndMagneticClass('file_prefix', sampleRate=1)
# derived_instance.plot()
