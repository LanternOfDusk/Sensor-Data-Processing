import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ErrorDataClass extends DataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_Errors.csv";
    private List<Integer> code = new ArrayList<>();
    private List<String> message = new ArrayList<>();

    // Public methods
    public ErrorDataClass(String fileNamePrefix) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(" ");
                code.add(Integer.parseInt(parts[0]));
                message.add(parts[1]);
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
