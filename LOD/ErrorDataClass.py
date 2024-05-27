import pandas as pd
from DataBaseClass import DataBaseClass  # 이미 구현된 DataBaseClass를 import합니다.

class ErrorDataClass(DataBaseClass):
    def __init__(self, fileNamePrefix):
        super().__init__()
        self.FileNameAppendage = '_Errors.csv'
        self.Code = []
        self.Message = []

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        file_name = self.create_file_name(fileNamePrefix)
        data = pd.read_csv(file_name, delimiter=',', header=0)
        self.Code = data.iloc[:, 1].tolist()
        self.Message = data.iloc[:, 2].tolist()

# 사용 예:
# fileNamePrefix = 'example_prefix'
# error_data = ErrorDataClass(fileNamePrefix)
# print(error_data.Code)
# print(error_data.Message)
