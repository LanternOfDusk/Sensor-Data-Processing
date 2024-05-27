import pandas as pd
from DataBaseClass import DataBaseClass  # 이미 구현된 DataBaseClass를 import합니다.

class RegisterDataClass(DataBaseClass):
    def __init__(self, fileNamePrefix):
        super().__init__()
        self.FileNameAppendage = '_Registers.csv'
        self.Address = []
        self.Value = []
        self.FloatValue = []
        self.Name = []

        self.import_data(fileNamePrefix)

    def import_data(self, fileNamePrefix):
        file_name = self.create_file_name(fileNamePrefix)
        data = pd.read_csv(file_name, delimiter=',', header=None, skiprows=1)
        self.Address = data.iloc[:, 1].tolist()
        self.Value = data.iloc[:, 2].tolist()
        self.FloatValue = data.iloc[:, 3].tolist()
        self.Name = data.iloc[:, 4].tolist()

    def get_value_at_address(self, address):
        indexes = self.indexes_of_address(address)
        return self.value_at_indexes(indexes)

    def get_float_value_at_address(self, address):
        indexes = self.indexes_of_address(address)
        return self.float_value_at_indexes(indexes)

    def get_value_at_name(self, name):
        indexes = self.indexes_of_name(name)
        return self.value_at_indexes(indexes)

    def get_float_value_at_name(self, name):
        indexes = self.indexes_of_name(name)
        return self.float_value_at_indexes(indexes)

    def indexes_of_address(self, address):
        indexes = [i for i, addr in enumerate(self.Address) if addr == address]
        if not indexes:
            raise ValueError('Register address not found.')
        return indexes

    def indexes_of_name(self, name):
        indexes = [i for i, n in enumerate(self.Name) if n == name]
        if not indexes:
            raise ValueError('Register name not found.')
        return indexes

    def value_at_indexes(self, indexes):
        values = [self.Value[i] for i in indexes]
        if len(set(values)) > 1:
            raise ValueError('Conflicting register values exist.')
        return values[0]

    def float_value_at_indexes(self, indexes):
        float_values = [self.FloatValue[i] for i in indexes]
        if len(set(float_values)) > 1:
            raise ValueError('Conflicting register values exist.')
        return float_values[0]

# 사용 예:
# fileNamePrefix = 'example_prefix'
# register_data = RegisterDataClass(fileNamePrefix)
# value_at_address = register_data.get_value_at_address(67)
# print(value_at_address)
