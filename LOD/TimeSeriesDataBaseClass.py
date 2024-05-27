import numpy as np
from DataBaseClass import DataBaseClass  # DataBaseClass가 구현된 파일을 import 합니다.

class TimeSeriesDataBaseClass(DataBaseClass):
    def __init__(self):
        super().__init__()
        self._time = np.array([])
        self._sample_period = 0
        self._sample_rate = 0
        self._start_time = 0
        self.time_axis = 'Sample'

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        self._sample_rate = sample_rate
        if self._sample_rate == 0:
            self._time = np.array([])
            self.time_axis = 'Sample'
        elif self.NumPackets != 0:
            self._time = np.arange(self.NumPackets) * (1 / self._sample_rate) + self._start_time
            self.time_axis = 'Time (s)'

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time
        self.sample_rate = self._sample_rate  # Update time vector based on new start time

    @property
    def sample_period(self):
        if self._sample_rate == 0:
            return 0
        else:
            return 1 / self._sample_rate

    @property
    def time(self):
        return self._time

    def plot(self):
        raise NotImplementedError("Subclasses should implement this!")

# Example usage:
# class DerivedTimeSeriesClass(TimeSeriesDataBaseClass):
#     def __init__(self, fileNamePrefix, sampleRate):
#         super().__init__()
#         self.FileNameAppendage = '_example.csv'
#         self.sample_rate = sampleRate
#         self.import_csv_numeric(fileNamePrefix)
#
#     def plot(self):
#         print("Plotting data...")
#
# derived_instance = DerivedTimeSeriesClass('file_prefix', sampleRate=1)
# derived_instance.plot()
