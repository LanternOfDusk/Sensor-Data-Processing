import pandas as pd
import os

class DataBaseClass:
    def __init__(self):
        self.NumPackets = 0
        self.PacketNumber = []

    def import_csv_numeric(self, fileNamePrefix):
        file_name = self.create_file_name(fileNamePrefix)
        data = pd.read_csv(file_name, header=None, skiprows=1).values
        self.PacketNumber = data[:, 0]
        self.NumPackets = len(self.PacketNumber)
        return data

    def import_csv_mixed(self, fileNamePrefix, field_specifier):
        file_name = self.create_file_name(fileNamePrefix)
        data = pd.read_csv(file_name, header=0)
        self.PacketNumber = data.iloc[:, 0].tolist()
        self.NumPackets = len(self.PacketNumber)
        return data

    def create_fig_name(self):
        name, ext = os.path.splitext(self.FileNameAppendage)
        fig_name = name[1:]  # Removing the first character (assumed to be an underscore)
        return fig_name

    def create_file_name(self, fileNamePrefix):
        file_name = fileNamePrefix + self.FileNameAppendage
        if not os.path.exists(file_name):
            raise FileNotFoundError('File not found. No data was imported.')
        return file_name

# Example usage:
# class DerivedClass(DataBaseClass):
#     def __init__(self, fileNamePrefix):
#         super().__init__()
#         self.FileNameAppendage = '_example.csv'
#         self.import_csv_numeric(fileNamePrefix)
#
# derived_instance = DerivedClass('file_prefix')
