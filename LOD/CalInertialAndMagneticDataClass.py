import pandas as pd
from InertialAndMagneticDataBaseClass import InertialAndMagneticDataBaseClass  # 이미 구현된 InertialAndMagneticDataBaseClass를 import합니다.

class CalInertialAndMagneticDataClass(InertialAndMagneticDataBaseClass):
    def __init__(self, fileNamePrefix, **kwargs):
        super().__init__()
        self.FileNameAppendage = '_CalInertialAndMag.csv'
        
        for key, value in kwargs.items():
            if key == 'SampleRate':
                self.sample_rate = value
            else:
                raise ValueError('Invalid argument.')

        self.import_data(fileNamePrefix)

        # Set protected parent class variables
        self.GyroscopeUnits = '°/s'
        self.AccelerometerUnits = 'g'
        self.MagnetometerUnits = 'G'

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

# 사용 예:
# fileNamePrefix = 'example_prefix'
# cal_data = CalInertialAndMagneticDataClass(fileNamePrefix, SampleRate=1)
# cal_data.plot()
