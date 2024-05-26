import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class RawInertialAndMagneticDataClass extends InertialAndMagneticDataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_RawInertialAndMag.csv";

    // Public methods
    public RawInertialAndMagneticDataClass(String fileNamePrefix, int sampleRate) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                // Process raw inertial and magnetic data
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Set protected parent class variables
        setGyroscopeUnits("lsb");
        setAccelerometerUnits("lsb");
        setMagnetometerUnits("lsb");

        setSampleRate(sampleRate);
    }
}
