import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class RawBatteryAndThermometerDataClass extends BatteryAndThermometerDataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_RawBattAndTherm.csv";

    // Public methods
    public RawBatteryAndThermometerDataClass(String fileNamePrefix, int sampleRate) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                // Process raw battery and thermometer data
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Set protected parent class variables
        setThermometerUnits("lsb");
        setBatteryUnits("lsb");

        setSampleRate(sampleRate);
    }
}
