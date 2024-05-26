import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CalInertialAndMagneticDataClass extends InertialAndMagneticDataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_CalInertialAndMag.csv";

    // Public methods
    public CalInertialAndMagneticDataClass(String fileNamePrefix, int sampleRate) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                // Process calibrated inertial and magnetic data
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Set protected parent class variables
        setGyroscopeUnits("°/s");
        setAccelerometerUnits("g");
        setMagnetometerUnits("G");

        setSampleRate(sampleRate);
    }
}
