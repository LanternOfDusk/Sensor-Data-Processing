import pandas as pd
from DataBaseClass import DataBaseClass  # 이미 구현된 DataBaseClass를 import합니다.

class PWMoutputDataClass(DataBaseClass):
    def __init__(self, fileNamePrefix):
        super().__init__()
        self.FileNameAppendage = '_PWMoutput.csv'
        self.AX0 = []
        self.AX2 = []
        self.AX4 = []
        self.AX6 = []

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        data = self.import_csv_numeric(fileNamePrefix)
        self.AX0 = data[:, 1]
        self.AX2 = data[:, 2]
        self.AX4 = data[:, 3]
        self.AX6 = data[:, 4]

# 사용 예:
# fileNamePrefix = 'example_prefix'
# pwm_output_data = PWMoutputDataClass(fileNamePrefix)
# print(pwm_output_data.AX0)
# print(pwm_output_data.AX2)
# print(pwm_output_data.AX4)
# print(pwm_output_data.AX6)
