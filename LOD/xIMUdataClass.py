from ErrorDataClass import ErrorDataClass
from CommandDataClass import CommandDataClass
from RegisterDataClass import RegisterDataClass
from DateTimeDataClass import DateTimeDataClass
from RawBatteryAndThermometerDataClass import RawBatteryAndThermometerDataClass
from CalBatteryAndThermometerDataClass import CalBatteryAndThermometerDataClass
from RawInertialAndMagneticDataClass import RawInertialAndMagneticDataClass
from CalInertialAndMagneticDataClass import CalInertialAndMagneticDataClass
from QuaternionDataClass import QuaternionDataClass
from EulerAnglesDataClass import EulerAnglesDataClass
from RotationMatrixDataClass import RotationMatrixDataClass
from DigitalIOdataClass import DigitalIOdataClass
from RawAnalogueInputDataClass import RawAnalogueInputDataClass
from CalAnalogueInputDataClass import CalAnalogueInputDataClass
from PWMoutputDataClass import PWMoutputDataClass
from RawADXL345busDataClass import RawADXL345busDataClass
from CalADXL345busDataClass import CalADXL345busDataClass

class xIMUdataClass:
    def __init__(self, fileNamePrefix, **kwargs):
        self.FileNamePrefix = fileNamePrefix
        self.ErrorData = None
        self.CommandData = None
        self.RegisterData = None
        self.DateTimeData = None
        self.RawBatteryAndThermometerData = None
        self.CalBatteryAndThermometerData = None
        self.RawInertialAndMagneticData = None
        self.CalInertialAndMagneticData = None
        self.QuaternionData = None
        self.EulerAnglesData = None
        self.RotationMatrixData = None
        self.DigitalIOdata = None
        self.RawAnalogueInputData = None
        self.CalAnalogueInputData = None
        self.PWMoutputData = None
        self.RawADXL345busData = None
        self.CalADXL345busData = None
        
        # Create data objects from files
        dataImported = False
        try:
            self.ErrorData = ErrorDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.CommandData = CommandDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.RegisterData = RegisterDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.DateTimeData = DateTimeDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.RawBatteryAndThermometerData = RawBatteryAndThermometerDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.CalBatteryAndThermometerData = CalBatteryAndThermometerDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.RawInertialAndMagneticData = RawInertialAndMagneticDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.CalInertialAndMagneticData = CalInertialAndMagneticDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.QuaternionData = QuaternionDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.EulerAnglesData = EulerAnglesDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.RotationMatrixData = RotationMatrixDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.DigitalIOdata = DigitalIOdataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.RawAnalogueInputData = RawAnalogueInputDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.CalAnalogueInputData = CalAnalogueInputDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.PWMoutputData = PWMoutputDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.RawADXL345busData = RawADXL345busDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        try:
            self.CalADXL345busData = CalADXL345busDataClass(fileNamePrefix)
            dataImported = True
        except Exception:
            pass
        
        if not dataImported:
            raise ValueError('No data was imported.')

        # Apply SampleRate from register data
        try:
            self.DateTimeData.SampleRate = self.SampleRateFromRegValue(self.RegisterData.GetValueAtAddress(67))
        except Exception:
            pass
        try:
            sample_rate = self.SampleRateFromRegValue(self.RegisterData.GetValueAtAddress(68))
            self.RawBatteryAndThermometerData.SampleRate = sample_rate
            self.CalBatteryAndThermometerData.SampleRate = sample_rate
        except Exception:
            pass
        try:
            sample_rate = self.SampleRateFromRegValue(self.RegisterData.GetValueAtAddress(69))
            self.RawInertialAndMagneticData.SampleRate = sample_rate
            self.CalInertialAndMagneticData.SampleRate = sample_rate
        except Exception:
            pass
        try:
            sample_rate = self.SampleRateFromRegValue(self.RegisterData.GetValueAtAddress(70))
            self.QuaternionData.SampleRate = sample_rate
            self.RotationMatrixData.SampleRate = sample_rate
            self.EulerAnglesData.SampleRate = sample_rate
        except Exception:
            pass
        try:
            self.DigitalIOdata.SampleRate = self.SampleRateFromRegValue(self.RegisterData.GetValueAtAddress(78))
        except Exception:
            pass
        try:
            sample_rate = self.SampleRateFromRegValue(self.RegisterData.GetValueAtAddress(80))
            self.RawAnalogueInputData.SampleRate = sample_rate
            self.CalAnalogueInputData.SampleRate = sample_rate
        except Exception:
            pass
        try:
            sample_rate = self.SampleRateFromRegValue(self.RegisterData.GetValueAtAddress(85))
            self.RawADXL345busData.SampleRate = sample_rate
            self.CalADXL345busData.SampleRate = sample_rate
        except Exception:
            pass

        # Apply SampleRate if specified as argument
        for key, value in kwargs.items():
            if key == 'DateTimeSampleRate':
                try:
                    self.DateTimeData.SampleRate = value
                except Exception:
                    pass
            elif key == 'BattThermSampleRate':
                try:
                    self.RawBatteryAndThermometerData.SampleRate = value
                    self.CalBatteryAndThermometerData.SampleRate = value
                except Exception:
                    pass
            elif key == 'InertialMagneticSampleRate':
                try:
                    self.RawInertialAndMagneticData.SampleRate = value
                    self.CalInertialAndMagneticData.SampleRate = value
                except Exception:
                    pass
            elif key == 'QuaternionSampleRate':
                try:
                    self.QuaternionData.SampleRate = value
                    self.RotationMatrixData.SampleRate = value
                    self.EulerAnglesData.SampleRate = value
                except Exception:
                    pass
            elif key == 'DigitalIOSampleRate':
                try:
                    self.DigitalIOdata.SampleRate = value
                except Exception:
                    pass
            elif key == 'AnalogueInputSampleRate':
                try:
                    self.RawAnalogueInputData.SampleRate = value
                    self.CalAnalogueInputData.SampleRate = value
                except Exception:
                    pass
            elif key == 'ADXL345SampleRate':
                try:
                    self.RawADXL345busData.SampleRate = value
                    self.CalADXL345busData.SampleRate = value
                except Exception:
                    pass
            else:
                raise ValueError('Invalid argument.')

    def plot(self):
        try:
            self.RawBatteryAndThermometerData.plot()
        except Exception:
            pass
        try:
            self.CalBatteryAndThermometerData.plot()
        except Exception:
            pass
        try:
            self.RawInertialAndMagneticData.plot()
        except Exception:
            pass
        try:
            self.CalInertialAndMagneticData.plot()
        except Exception:
            pass
        try:
            self.QuaternionData.plot()
        except Exception:
            pass
        try:
            self.EulerAnglesData.plot()
        except Exception:
            pass
        try:
            self.RotationMatrixData.plot()
        except Exception:
            pass
        try:
            self.DigitalIOdata.plot()
        except Exception:
            pass
        try:
            self.RawAnalogueInputData.plot()
        except Exception:
            pass
        try:
            self.CalAnalogueInputData.plot()
        except Exception:
            pass
        try:
            self.RawADXL345busData.plot()
        except Exception:
            pass
        try:
            self.CalADXL345busData.plot()
        except Exception:
            pass

    def SampleRateFromRegValue(self, value):
        return 2 ** (value - 1)

# 사용 예:
# fileNamePrefix = 'example_prefix'
# imu_data = xIMUdataClass(fileNamePrefix, DateTimeSampleRate=1, BattThermSampleRate=2)
# imu_data.plot()
