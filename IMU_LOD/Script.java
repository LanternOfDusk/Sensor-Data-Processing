import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        // 데이터 불러오기
        xIMUdata xIMUdata = new xIMUdata("LoggedData/LoggedData");

        double samplePeriod = 1.0 / 256.0;

        double[][] gyr = xIMUdata.getGyroscopeData(); // Get gyroscope data
        double[][] acc = xIMUdata.getAccelerometerData(); // Get accelerometer data

        // AHRS 알고리즘 적용
        MahonyAHRS ahrs = new MahonyAHRS(samplePeriod, 1, 0);
        int dataLength = gyr.length;
        double[][][] R = new double[dataLength][3][3]; // Rotation matrix

        for (int i = 0; i < dataLength; i++) {
            double[] gyrRad = Arrays.stream(gyr[i]).map(g -> g * (Math.PI / 180.0)).toArray(); // Convert to radians
            ahrs.updateIMU(gyrRad, acc[i]);
            R[i] = ahrs.quaternionToRotationMatrix();
        }

        // Tilt-compensated accelerometer 계산
        double[][] tcAcc = new double[dataLength][3];

        for (int i = 0; i < dataLength; i++) {
            tcAcc[i] = matrixVectorMultiply(R[i], acc[i]);
        }

        // Linear acceleration 계산 (중력 제거)
        double[][] linAcc = new double[dataLength][3];
        for (int i = 0; i < dataLength; i++) {
            linAcc[i][0] = tcAcc[i][0] * 9.81;
            linAcc[i][1] = tcAcc[i][1] * 9.81;
            linAcc[i][2] = (tcAcc[i][2] - 1) * 9.81;
        }

        // Linear velocity 계산 (가속도 적분)
        double[][] linVel = new double[dataLength][3];
        for (int i = 1; i < dataLength; i++) {
            linVel[i][0] = linVel[i - 1][0] + linAcc[i][0] * samplePeriod;
            linVel[i][1] = linVel[i - 1][1] + linAcc[i][1] * samplePeriod;
            linVel[i][2] = linVel[i - 1][2] + linAcc[i][2] * samplePeriod;
        }

        // High-pass filter linear velocity to remove drift
        double[][] linVelHP = highPassFilter(linVel, samplePeriod, 0.1);

        // Linear position 계산 (속도 적분)
        double[][] linPos = new double[dataLength][3];
        for (int i = 1; i < dataLength; i++) {
            linPos[i][0] = linPos[i - 1][0] + linVelHP[i][0] * samplePeriod;
            linPos[i][1] = linPos[i - 1][1] + linVelHP[i][1] * samplePeriod;
            linPos[i][2] = linPos[i - 1][2] + linVelHP[i][2] * samplePeriod;
        }

        // High-pass filter linear position to remove drift
        double[][] linPosHP = highPassFilter(linPos, samplePeriod, 0.1);

        // 결과 출력
        System.out.println("Linear Position (High-pass filtered):");
        for (int i = 0; i < linPosHP.length; i++) {
            System.out.printf("%f %f %f\n", linPosHP[i][0], linPosHP[i][1], linPosHP[i][2]);
        }
    }

    public static double[] matrixVectorMultiply(double[][] matrix, double[] vector) {
        double[] result = new double[3];
        for (int i = 0; i < 3; i++) {
            result[i] = matrix[i][0] * vector[0] + matrix[i][1] * vector[1] + matrix[i][2] * vector[2];
        }
        return result;
    }

    public static double[][] highPassFilter(double[][] data, double samplePeriod, double cutOffFrequency) {
        int order = 1;
        double rc = 1.0 / (2 * Math.PI * cutOffFrequency);
        double dt = samplePeriod;
        double alpha = rc / (rc + dt);
        double[][] filteredData = new double[data.length][3];

        filteredData[0] = data[0];
        for (int i = 1; i < data.length; i++) {
            for (int j = 0; j < 3; j++) {
                filteredData[i][j] = alpha * (filteredData[i - 1][j] + data[i][j] - data[i - 1][j]);
            }
        }
        return filteredData;
    }
}

class MahonyAHRS {
    private double samplePeriod;
    private double kp;
    private double ki;
    private double[] quaternion;
    private double[] eInt;

    public MahonyAHRS(double samplePeriod, double kp, double ki) {
        this.samplePeriod = samplePeriod;
        this.kp = kp;
        this.ki = ki;
        this.quaternion = new double[]{1, 0, 0, 0};
        this.eInt = new double[]{0, 0, 0};
    }

    public void updateIMU(double[] gyroscope, double[] accelerometer) {
        double[] q = this.quaternion;

        if (norm(accelerometer) == 0) return;
        accelerometer = normalize(accelerometer);

        double[] v = {
            2 * (q[1] * q[3] - q[0] * q[2]),
            2 * (q[0] * q[1] + q[2] * q[3]),
            q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]
        };

        double[] e = cross(accelerometer, v);
        if (this.ki > 0) {
            this.eInt = vectorAdd(this.eInt, scalarMultiply(e, this.samplePeriod));
        } else {
            this.eInt = new double[]{0, 0, 0};
        }

        gyroscope = vectorAdd(gyroscope, vectorAdd(scalarMultiply(e, this.kp), scalarMultiply(this.eInt, this.ki)));
        double[] qDot = scalarMultiply(quaternProd(q, new double[]{0, gyroscope[0], gyroscope[1], gyroscope[2]}), 0.5);
        q = vectorAdd(q, scalarMultiply(qDot, this.samplePeriod));
        this.quaternion = normalize(q);
    }

    public double[][] quaternionToRotationMatrix() {
        double[] q = this.quaternion;
        double[][] R = new double[3][3];

        R[0][0] = 1 - 2 * (q[2] * q[2] + q[3] * q[3]);
        R[0][1] = 2 * (q[1] * q[2] - q[0] * q[3]);
        R[0][2] = 2 * (q[1] * q[3] + q[0] * q[2]);

        R[1][0] = 2 * (q[1] * q[2] + q[0] * q[3]);
        R[1][1] = 1 - 2 * (q[1] * q[1] + q[3] * q[3]);
        R[1][2] = 2 * (q[2] * q[3] - q[0] * q[1]);

        R[2][0] = 2 * (q[1] * q[3] - q[0] * q[2]);
        R[2][1] = 2 * (q[2] * q[3] + q[0] * q[1]);
        R[2][2] = 1 - 2 * (q[1] * q[1] + q[2] * q[2]);

        return R;
    }

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

