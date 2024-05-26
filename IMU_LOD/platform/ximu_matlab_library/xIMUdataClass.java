import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class xIMUdataClass {

    // Public properties
    private String fileNamePrefix = "";
    private Object errorData;
    private Object commandData;
    private Object registerData;
    private Object dateTimeData;
    private Object rawBatteryAndThermometerData;
    private Object calBatteryAndThermometerData;
    private Object rawInertialAndMagneticData;
    private Object calInertialAndMagneticData;
    private Object quaternionData;
    private Object rotationMatrixData;
    private Object eulerAnglesData;
    private Object digitalIOdata;
    private Object rawAnalogueInputData;
    private Object calAnalogueInputData;
    private Object pwmOutputData;
    private Object rawADXL345busData;
    private Object calADXL345busData;

    // Constructor
    public xIMUdataClass(String fileNamePrefix, Object... args) {
        this.fileNamePrefix = fileNamePrefix;
        boolean dataImported = false;

        // Try to import each data class
        try {
            errorData = new ErrorDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            commandData = new CommandDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            registerData = new RegisterDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            dateTimeData = new DateTimeDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            rawBatteryAndThermometerData = new RawBatteryAndThermometerDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            calBatteryAndThermometerData = new CalBatteryAndThermometerDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            rawInertialAndMagneticData = new RawInertialAndMagneticDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            calInertialAndMagneticData = new CalInertialAndMagneticDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            quaternionData = new QuaternionDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            eulerAnglesData = new EulerAnglesDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            rotationMatrixData = new RotationMatrixDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            digitalIOdata = new DigitalIOdataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            rawAnalogueInputData = new RawAnalogueInputDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            calAnalogueInputData = new CalAnalogueInputDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            pwmOutputData = new PWMoutputDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            rawADXL345busData = new RawADXL345busDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }
        try {
            calADXL345busData = new CalADXL345busDataClass(fileNamePrefix);
            dataImported = true;
        } catch (Exception e) { }

        if (!dataImported) {
            throw new RuntimeException("No data was imported.");
        }

        // Apply SampleRate from register data
        applySampleRates();

        // Apply SampleRate if specified as argument
        for (int i = 1; i < args.length; i += 2) {
            String sampleRateType = (String) args[i];
            int sampleRateValue = (Integer) args[i + 1];
            applySampleRate(sampleRateType, sampleRateValue);
        }
    }

    // Method to apply SampleRate from register data
    private void applySampleRates() {
        try {
            ((DateTimeDataClass) dateTimeData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(67)));
        } catch (Exception e) { }
        try {
            ((RawBatteryAndThermometerDataClass) rawBatteryAndThermometerData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(68)));
        } catch (Exception e) { }
        try {
            ((CalBatteryAndThermometerDataClass) calBatteryAndThermometerData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(68)));
        } catch (Exception e) { }
        try {
            ((RawInertialAndMagneticDataClass) rawInertialAndMagneticData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(69)));
        } catch (Exception e) { }
        try {
            ((CalInertialAndMagneticDataClass) calInertialAndMagneticData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(69)));
        } catch (Exception e) { }
        try {
            ((QuaternionDataClass) quaternionData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(70)));
        } catch (Exception e) { }
        try {
            ((RotationMatrixDataClass) rotationMatrixData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(70)));
        } catch (Exception e) { }
        try {
            ((EulerAnglesDataClass) eulerAnglesData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(70)));
        } catch (Exception e) { }
        try {
            ((DigitalIOdataClass) digitalIOdata).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(78)));
        } catch (Exception e) { }
        try {
            ((RawAnalogueInputDataClass) rawAnalogueInputData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(80)));
        } catch (Exception e) { }
        try {
            ((CalAnalogueInputDataClass) calAnalogueInputData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(80)));
        } catch (Exception e) { }
        try {
            ((RawADXL345busDataClass) rawADXL345busData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(85)));
        } catch (Exception e) { }
        try {
            ((CalADXL345busDataClass) calADXL345busData).setSampleRate(sampleRateFromRegValue(getRegisterDataValue(85)));
        } catch (Exception e) { }
    }

    // Method to get value at specific register address
    private int getRegisterDataValue(int address) {
        return ((RegisterDataClass) registerData).getValueAtAddress(address);
    }

    // Method to apply SampleRate if specified as argument
    private void applySampleRate(String sampleRateType, int sampleRateValue) {
        try {
            switch (sampleRateType) {
                case "DateTimeSampleRate":
                    ((DateTimeDataClass) dateTimeData).setSampleRate(sampleRateValue);
                    break;
                case "BattThermSampleRate":
                    ((RawBatteryAndThermometerDataClass) rawBatteryAndThermometerData).setSampleRate(sampleRateValue);
                    ((CalBatteryAndThermometerDataClass) calBatteryAndThermometerData).setSampleRate(sampleRateValue);
                    break;
                case "InertialMagneticSampleRate":
                    ((RawInertialAndMagneticDataClass) rawInertialAndMagneticData).setSampleRate(sampleRateValue);
                    ((CalInertialAndMagneticDataClass) calInertialAndMagneticData).setSampleRate(sampleRateValue);
                    break;
                case "QuaternionSampleRate":
                    ((QuaternionDataClass) quaternionData).setSampleRate(sampleRateValue);
                    ((RotationMatrixDataClass) rotationMatrixData).setSampleRate(sampleRateValue);
                    ((EulerAnglesDataClass) eulerAnglesData).setSampleRate(sampleRateValue);
                    break;
                case "DigitalIOSampleRate":
                    ((DigitalIOdataClass) digitalIOdata).setSampleRate(sampleRateValue);
                    break;
                case "AnalogueInputSampleRate":
                    ((RawAnalogueInputDataClass) rawAnalogueInputData).setSampleRate(sampleRateValue);
                    ((CalAnalogueInputDataClass) calAnalogueInputData).setSampleRate(sampleRateValue);
                    break;
                case "ADXL345SampleRate":
                    ((RawADXL345busDataClass) rawADXL345busData).setSampleRate(sampleRateValue);
                    ((CalADXL345busDataClass) calADXL345busData).setSampleRate(sampleRateValue);
                    break;
                default:
                    throw new IllegalArgumentException("Invalid argument.");
            }
        } catch (Exception e) {
            throw new RuntimeException("Error setting sample rate: " + e.getMessage());
        }
    }

    // Method to convert register value to sample rate
    private int sampleRateFromRegValue(int value) {
        return (int) Math.floor(Math.pow(2, value - 1));
    }

    // Method to plot data
    public void plot() {
        try {
            ((RawBatteryAndThermometerDataClass) rawBatteryAndThermometerData).plot();
        } catch (Exception e) { }
        try {
            ((CalBatteryAndThermometerDataClass) calBatteryAndThermometerData).plot();
        } catch (Exception e) { }
        try {
            ((RawInertialAndMagneticDataClass) rawInertialAndMagneticData).plot();
        } catch (Exception e) { }
        try {
            ((CalInertialAndMagneticDataClass) calInertialAndMagneticData).plot();
        } catch (Exception e) { }
        try {
            ((QuaternionDataClass) quaternionData).plot();
        } catch (Exception e) { }
        try {
            ((EulerAnglesDataClass) eulerAnglesData).plot();
        } catch (Exception e) { }
        try {
            ((RotationMatrixDataClass) rotationMatrixData).plot();
        } catch (Exception e) { }
        try {
            ((DigitalIOdataClass) digitalIOdata).plot();
        } catch (Exception e) { }
        try {
            ((RawAnalogueInputDataClass) rawAnalogueInputData).plot();
        } catch (Exception e) { }
        try {
            ((CalAnalogueInputDataClass) calAnalogueInputData).plot();
        } catch (Exception e) { }
        try {
            ((RawADXL345busDataClass) rawADXL345busData).plot();
        } catch (Exception e) { }
        try {
            ((CalADXL345busDataClass) calADXL345busData).plot();
        } catch (Exception e) { }
    }

    // Main method for testing
    public static void main(String[] args) {
        // Example usage
        xIMUdataClass imuData = new xIMUdataClass("filePrefix", "DateTimeSampleRate", 100);
        imuData.plot();
    }
}
