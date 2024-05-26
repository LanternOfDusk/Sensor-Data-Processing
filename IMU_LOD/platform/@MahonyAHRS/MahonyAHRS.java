public class MahonyAHRS {
    // Public properties
    public double samplePeriod = 1.0 / 256.0;
    public double[] quaternion = {1, 0, 0, 0}; // output quaternion describing the Earth relative to the sensor
    public double kp = 1; // algorithm proportional gain
    public double ki = 0; // algorithm integral gain
    
    // Private properties
    private double[] eInt = {0, 0, 0}; // integral error

    // Constructor
    public MahonyAHRS(Object... args) {
        for (int i = 0; i < args.length; i += 2) {
            if (args[i].equals("SamplePeriod")) {
                this.samplePeriod = (double) args[i + 1];
            } else if (args[i].equals("Quaternion")) {
                this.quaternion = (double[]) args[i + 1];
            } else if (args[i].equals("Kp")) {
                this.kp = (double) args[i + 1];
            } else if (args[i].equals("Ki")) {
                this.ki = (double) args[i + 1];
            } else {
                throw new IllegalArgumentException("Invalid argument");
            }
        }
    }

    public void update(double[] gyroscope, double[] accelerometer, double[] magnetometer) {
        double[] q = this.quaternion; // short name local variable for readability

        // Normalize accelerometer measurement
        if (norm(accelerometer) == 0) return; // handle NaN
        accelerometer = normalize(accelerometer); // normalize magnitude

        // Normalize magnetometer measurement
        if (norm(magnetometer) == 0) return; // handle NaN
        magnetometer = normalize(magnetometer); // normalize magnitude

        // Reference direction of Earth's magnetic field
        double[] h = quaternProd(q, quaternProd(new double[]{0, magnetometer[0], magnetometer[1], magnetometer[2]}, quaternConj(q)));
        double[] b = {0, norm(new double[]{h[1], h[2]}), 0, h[3]};

        // Estimated direction of gravity and magnetic field
        double[] v = {
            2 * (q[1] * q[3] - q[0] * q[2]),
            2 * (q[0] * q[1] + q[2] * q[3]),
            q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]
        };
        double[] w = {
            2 * b[1] * (0.5 - q[2] * q[2] - q[3] * q[3]) + 2 * b[3] * (q[1] * q[3] - q[0] * q[2]),
            2 * b[1] * (q[1] * q[2] - q[0] * q[3]) + 2 * b[3] * (q[0] * q[1] + q[2] * q[3]),
            2 * b[1] * (q[0] * q[2] + q[1] * q[3]) + 2 * b[3] * (0.5 - q[1] * q[1] - q[2] * q[2])
        };

        // Error is sum of cross product between estimated direction and measured direction of fields
        double[] e = vectorAdd(cross(accelerometer, v), cross(magnetometer, w));
        if (this.ki > 0) {
            this.eInt = vectorAdd(this.eInt, scalarMultiply(e, this.samplePeriod));
        } else {
            this.eInt = new double[]{0, 0, 0};
        }

        // Apply feedback terms
        gyroscope = vectorAdd(gyroscope, vectorAdd(scalarMultiply(e, this.kp), scalarMultiply(this.eInt, this.ki)));

        // Compute rate of change of quaternion
        double[] qDot = scalarMultiply(quaternProd(q, new double[]{0, gyroscope[0], gyroscope[1], gyroscope[2]}), 0.5);

        // Integrate to yield quaternion
        q = vectorAdd(q, scalarMultiply(qDot, this.samplePeriod));
        this.quaternion = normalize(q); // normalize quaternion
    }

    public void updateIMU(double[] gyroscope, double[] accelerometer) {
        double[] q = this.quaternion; // short name local variable for readability

        // Normalize accelerometer measurement
        if (norm(accelerometer) == 0) return; // handle NaN
        accelerometer = normalize(accelerometer); // normalize magnitude

        // Estimated direction of gravity and magnetic flux
        double[] v = {
            2 * (q[1] * q[3] - q[0] * q[2]),
            2 * (q[0] * q[1] + q[2] * q[3]),
            q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]
        };

        // Error is sum of cross product between estimated direction and measured direction of field
        double[] e = cross(accelerometer, v);
        if (this.ki > 0) {
            this.eInt = vectorAdd(this.eInt, scalarMultiply(e, this.samplePeriod));
        } else {
            this.eInt = new double[]{0, 0, 0};
        }

        // Apply feedback terms
        gyroscope = vectorAdd(gyroscope, vectorAdd(scalarMultiply(e, this.kp), scalarMultiply(this.eInt, this.ki)));

        // Compute rate of change of quaternion
        double[] qDot = scalarMultiply(quaternProd(q, new double[]{0, gyroscope[0], gyroscope[1], gyroscope[2]}), 0.5);

        // Integrate to yield quaternion
        q = vectorAdd(q, scalarMultiply(qDot, this.samplePeriod));
        this.quaternion = normalize(q); // normalize quaternion
    }

    // Helper methods
    private double norm(double[] vec) {
        double sum = 0;
        for (double v : vec) {
            sum += v * v;
        }
        return Math.sqrt(sum);
    }

    private double[] normalize(double[] vec) {
        double norm = norm(vec);
        double[] normalized = new double[vec.length];
        for (int i = 0; i < vec.length; i++) {
            normalized[i] = vec[i] / norm;
        }
        return normalized;
    }

    private double[] quaternProd(double[] q1, double[] q2) {
        return new double[]{
            q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3],
            q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2],
            q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1],
            q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]
        };
    }

    private double[] quaternConj(double[] q) {
        return new double[]{q[0], -q[1], -q[2], -q[3]};
    }

    private double[] cross(double[] a, double[] b) {
        return new double[]{
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]
        };
    }

    private double[] vectorAdd(double[] a, double[] b) {
        double[] result = new double[a.length];
        for (int i = 0; i < a.length; i++) {
            result[i] = a[i] + b[i];
        }
        return result;
    }

    private double[] scalarMultiply(double[] vec, double scalar) {
        double[] result = new double[vec.length];
        for (int i = 0; i < vec.length; i++) {
            result[i] = vec[i] * scalar;
        }
        return result;
    }
}
