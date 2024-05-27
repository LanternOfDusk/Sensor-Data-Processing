import numpy as np

class MahonyAHRS:
    def __init__(self, SamplePeriod=1/256, Quaternion=[1, 0, 0, 0], Kp=1, Ki=0):
        self.SamplePeriod = SamplePeriod
        self.Quaternion = np.array(Quaternion, dtype=float)
        self.Kp = Kp
        self.Ki = Ki
        self.eInt = np.array([0, 0, 0], dtype=float)
        
    def quaternProd(self, a, b):
        """ Quaternion product of two quaternions """
        w1, x1, y1, z1 = a
        w2, x2, y2, z2 = b
        return np.array([
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        ], dtype=float)
    
    def quaternConj(self, q):
        """ Conjugate of a quaternion """
        q = np.array(q, dtype=float)
        return np.array([q[0], -q[1], -q[2], -q[3]], dtype=float)

    def update(self, Gyroscope, Accelerometer, Magnetometer):
        q = self.Quaternion

        if np.linalg.norm(Accelerometer) == 0:
            return
        Accelerometer = Accelerometer / np.linalg.norm(Accelerometer)

        if np.linalg.norm(Magnetometer) == 0:
            return
        Magnetometer = Magnetometer / np.linalg.norm(Magnetometer)

        h = self.quaternProd(q, self.quaternProd([0] + list(Magnetometer), self.quaternConj(q)))
        b = np.array([0, np.linalg.norm(h[1:3]), 0, h[3]], dtype=float)

        v = np.array([
            2*(q[1]*q[3] - q[0]*q[2]),
            2*(q[0]*q[1] + q[2]*q[3]),
            q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2
        ], dtype=float)
        
        w = np.array([
            2*b[1]*(0.5 - q[2]**2 - q[3]**2) + 2*b[3]*(q[1]*q[3] - q[0]*q[2]),
            2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3]),
            2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]**2 - q[2]**2)
        ], dtype=float)

        e = np.cross(Accelerometer, v) + np.cross(Magnetometer, w)
        
        if self.Ki > 0:
            self.eInt = self.eInt + e * self.SamplePeriod
        else:
            self.eInt = np.array([0, 0, 0], dtype=float)
        
        Gyroscope = Gyroscope + self.Kp * e + self.Ki * self.eInt
        qDot = 0.5 * self.quaternProd(q, [0] + list(Gyroscope))

        q = q + qDot * self.SamplePeriod
        self.Quaternion = q / np.linalg.norm(q)

    def updateIMU(self, Gyroscope, Accelerometer):
        q = self.Quaternion

        if np.linalg.norm(Accelerometer) == 0:
            return
        Accelerometer = Accelerometer / np.linalg.norm(Accelerometer)

        v = np.array([
            2*(q[1]*q[3] - q[0]*q[2]),
            2*(q[0]*q[1] + q[2]*q[3]),
            q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2
        ], dtype=float)

        e = np.cross(Accelerometer, v)
        
        if self.Ki > 0:
            self.eInt = self.eInt + e * self.SamplePeriod
        else:
            self.eInt = np.array([0, 0, 0], dtype=float)
        
        Gyroscope = Gyroscope + self.Kp * e + self.Ki * self.eInt
        qDot = 0.5 * self.quaternProd(q, [0] + list(Gyroscope))

        q = q + qDot * self.SamplePeriod
        self.Quaternion = q / np.linalg.norm(q)
