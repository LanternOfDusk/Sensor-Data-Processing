import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class RegisterDataClass extends DataBaseClass {
    // Public 'read-only' properties
    private String fileNameAppendage = "_Registers.csv";
    private List<Integer> address = new ArrayList<>();
    private List<Integer> value = new ArrayList<>();
    private List<Float> floatValue = new ArrayList<>();
    private List<String> name = new ArrayList<>();

    // Public methods
    public RegisterDataClass(String fileNamePrefix) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileNamePrefix + fileNameAppendage));
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(" ");
                address.add(Integer.parseInt(parts[0]));
                value.add(Integer.parseInt(parts[1]));
                floatValue.add(Float.parseFloat(parts[2]));
                name.add(parts[3]);
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public int getValueAtAddress(int address) {
        int index = indexesOfAddress(address);
        return value.get(index);
    }

    public float getFloatValueAtAddress(int address) {
        int index = indexesOfAddress(address);
        return floatValue.get(index);
    }

    public int getValueAtName(String name) {
        int index = indexesOfName(name);
        return value.get(index);
    }

    public float getFloatValueAtName(String name) {
        int index = indexesOfName(name);
        return floatValue.get(index);
    }

    // Private methods
    private int indexesOfAddress(int address) {
        int index = this.address.indexOf(address);
        if (index == -1) {
            throw new RuntimeException("Register address not found.");
        }
        return index;
    }

    private int indexesOfName(String name) {
        int index = this.name.indexOf(name);
        if (index == -1) {
            throw new RuntimeException("Register name not found.");
        }
        return index;
    }
}
