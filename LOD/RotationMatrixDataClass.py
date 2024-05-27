import numpy as np
import pandas as pd
from TimeSeriesDataBaseClass import TimeSeriesDataBaseClass  # 이미 구현된 TimeSeriesDataBaseClass를 import합니다.

class RotationMatrixDataClass(TimeSeriesDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_RotationMatrix.csv'
        self.RotationMatrix = None

        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.RotationMatrix = np.zeros((self.NumPackets, 3, 3))
        self.RotationMatrix[:, 0, 0] = data[:, 1]
        self.RotationMatrix[:, 0, 1] = data[:, 2]
        self.RotationMatrix[:, 0, 2] = data[:, 3]
        self.RotationMatrix[:, 1, 0] = data[:, 4]
        self.RotationMatrix[:, 1, 1] = data[:, 5]
        self.RotationMatrix[:, 1, 2] = data[:, 6]
        self.RotationMatrix[:, 2, 0] = data[:, 7]
        self.RotationMatrix[:, 2, 1] = data[:, 8]
        self.RotationMatrix[:, 2, 2] = data[:, 9]
        self.sample_rate = self.sample_rate  # 시간 벡터를 생성하기 위해 sample_rate 설정

    def plot(self):
        raise NotImplementedError("This method is unimplemented.")

# 사용 예:
# fileNamePrefix = 'example_prefix'
# rotation_matrix_data = RotationMatrixDataClass(fileNamePrefix, SampleRate=1)
# rotation_matrix_data.plot()
