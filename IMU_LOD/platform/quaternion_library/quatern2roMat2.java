public class Quatern2RotMat {
    // Converts a quaternion orientation to a rotation matrix
    public static double[][][] quatern2rotMat(double[][] q) {
        int n = q.length;
        double[][][] R = new double[3][3][n];

        for (int i = 0; i < n; i++) {
            R[0][0][i] = 2 * q[i][0] * q[i][0] - 1 + 2 * q[i][1] * q[i][1];
            R[0][1][i] = 2 * (q[i][1] * q[i][2] + q[i][0] * q[i][3]);
            R[0][2][i] = 2 * (q[i][1] * q[i][3] - q[i][0] * q[i][2]);
            R[1][0][i] = 2 * (q[i][1] * q[i][2] - q[i][0] * q[i][3]);
            R[1][1][i] = 2 * q[i][0] * q[i][0] - 1 + 2 * q[i][2] * q[i][2];
            R[1][2][i] = 2 * (q[i][2] * q[i][3] + q[i][0] * q[i][1]);
            R[2][0][i] = 2 * (q[i][1] * q[i][3] + q[i][0] * q[i][2]);
            R[2][1][i] = 2 * (q[i][2] * q[i][3] - q[i][0] * q[i][1]);
            R[2][2][i] = 2 * q[i][0] * q[i][0] - 1 + 2 * q[i][3] * q[i][3];
        }

        return R;
    }
}
