import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CalADXL345busDataClass extends ADXL345busDataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_CalADXL345bus.csv";

    // Public methods
    public CalADXL345busDataClass(String fileNamePrefix, int sampleRate) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                // Process calibrated ADXL345 bus data
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Set protected parent class variables
        setAccelerometerUnits("g");

        setSampleRate(sampleRate);
    }
}
