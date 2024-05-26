import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class PWMoutputDataClass extends DataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_PWMoutput.csv";
    private int[] AX0;
    private int[] AX2;
    private int[] AX4;
    private int[] AX6;

    // Public methods
    public PWMoutputDataClass(String fileNamePrefix) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                // Process PWM output data
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public int[] getAX0() {
        return AX0;
    }

    public int[] getAX2() {
        return AX2;
    }

    public int[] getAX4() {
        return AX4;
    }

    public int[] getAX6() {
        return AX6;
    }
}
