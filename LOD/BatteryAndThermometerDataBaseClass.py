import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class BatteryAndThermometerDataBaseClass(TimeSeriesDataBaseClass):
    def __init__(self):
        super().__init__()
        self.Battery = []
        self.Thermometer = []
        self.ThermometerUnits = ''
        self.BatteryUnits = ''

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.Battery = data[:, 1]
        self.Thermometer = data[:, 2]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

    def plot(self):
        if self.NumPackets == 0:
            raise ValueError('No data to plot.')
        else:
            time = np.arange(1, self.NumPackets + 1) if self.Time is None else self.Time
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, num=self.create_fig_name())

            ax1.plot(time, self.Battery)
            ax1.set_xlabel(self.time_axis)
            ax1.set_ylabel(f'Voltage ({self.BatteryUnits})')
            ax1.set_title('Battery Voltmeter')

            ax2.plot(time, self.Thermometer)
            ax2.set_xlabel(self.time_axis)
            ax2.set_ylabel(f'Temperature ({self.ThermometerUnits})')
            ax2.set_title('Thermometer')

            plt.show()

# 사용 예:
# class DerivedBatteryAndThermometerClass(BatteryAndThermometerDataBaseClass):
#     def __init__(self, fileNamePrefix, sampleRate):
#         super().__init__()
#         self.FileNameAppendage = '_example.csv'
#         self.sample_rate = sampleRate
#         self.import_data(fileNamePrefix)
#         self.ThermometerUnits = 'Celsius'
#         self.BatteryUnits = 'Volts'
#
# derived_instance = DerivedBatteryAndThermometerClass('file_prefix', sampleRate=1)
# derived_instance.plot()
