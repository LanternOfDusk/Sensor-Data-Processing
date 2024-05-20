import numpy as np

def quaternProd(q, r):
    """Compute the product of two quaternions."""
    return np.array([
        q[0] * r[0] - q[1] * r[1] - q[2] * r[2] - q[3] * r[3],
        q[0] * r[1] + q[1] * r[0] + q[2] * r[3] - q[3] * r[2],
        q[0] * r[2] - q[1] * r[3] + q[2] * r[0] + q[3] * r[1],
        q[0] * r[3] + q[1] * r[2] - q[2] * r[1] + q[3] * r[0]
    ])

def quaternConj(q):
    """Compute the conjugate of a quaternion."""
    return np.array([q[0], -q[1], -q[2], -q[3]])

def quatern2rotMat(q):
    """Convert a quaternion to a rotation matrix."""
    q0, q1, q2, q3 = q
    return np.array([
        [1 - 2*(q2**2 + q3**2), 2*(q1*q2 - q0*q3), 2*(q1*q3 + q0*q2)],
        [2*(q1*q2 + q0*q3), 1 - 2*(q1**2 + q3**2), 2*(q2*q3 - q0*q1)],
        [2*(q1*q3 - q0*q2), 2*(q2*q3 + q0*q1), 1 - 2*(q1**2 + q2**2)]
    ])

class MahonyAHRS:
    def __init__(self, sample_period=1/256, kp=1, ki=0):
        self.sample_period = sample_period
        self.quaternion = np.array([1, 0, 0, 0])
        self.kp = kp
        self.ki = ki
        self.e_int = np.array([0, 0, 0])

    def update_imu(self, gyroscope, accelerometer):
        q = self.quaternion

        # Normalise accelerometer measurement
        if np.linalg.norm(accelerometer) == 0:
            return
        accelerometer = accelerometer / np.linalg.norm(accelerometer)

        # Estimated direction of gravity
        v = np.array([
            2*(q[1]*q[3] - q[0]*q[2]),
            2*(q[0]*q[1] + q[2]*q[3]),
            q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2
        ])

        # Error is cross product between estimated direction and measured direction of field
        e = np.cross(accelerometer, v)
        if self.ki > 0:
            self.e_int += e * self.sample_period
        else:
            self.e_int = np.array([0, 0, 0])

        # Apply feedback terms
        gyroscope = gyroscope + self.kp * e + self.ki * self.e_int

        # Compute rate of change of quaternion
        q_dot = 0.5 * quaternProd(q, np.hstack([0, gyroscope]))

        # Integrate to yield quaternion
        q = q + q_dot * self.sample_period
        self.quaternion = q / np.linalg.norm(q)  # normalise quaternion
