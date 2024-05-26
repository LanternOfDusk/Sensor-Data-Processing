import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class RawAnalogueInputDataClass extends AnalogueInputDataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_RawAnalogueInput.csv";

    // Public methods
    public RawAnalogueInputDataClass(String fileNamePrefix, int sampleRate) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                // Process raw analogue input data
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Set protected parent class variables
        setADCunits("lsb");

        setSampleRate(sampleRate);
    }
}
