import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CalAnalogueInputDataClass extends AnalogueInputDataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_CalAnalogueInput.csv";

    // Public methods
    public CalAnalogueInputDataClass(String fileNamePrefix, int sampleRate) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                // Process calibrated analogue input data
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Set protected parent class variables
        setADCunits("V");

        setSampleRate(sampleRate);
    }
}
