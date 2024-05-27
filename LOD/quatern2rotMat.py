import sys
import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

def quatern2rotMat(q):
    """
    Converts a quaternion orientation to a rotation matrix.
    
    Args:
    q (numpy.ndarray): (4,) 형태의 쿼터니언 [w, x, y, z]

    Returns:
    numpy.ndarray: (3, 3) 형태의 회전 행렬
    """
    q = np.asarray(q)
    R = np.zeros((3, 3))
    
    R[0, 0] = 2 * q[0]**2 - 1 + 2 * q[1]**2
    R[0, 1] = 2 * (q[1] * q[2] + q[0] * q[3])
    R[0, 2] = 2 * (q[1] * q[3] - q[0] * q[2])
    R[1, 0] = 2 * (q[1] * q[2] - q[0] * q[3])
    R[1, 1] = 2 * q[0]**2 - 1 + 2 * q[2]**2
    R[1, 2] = 2 * (q[2] * q[3] + q[0] * q[1])
    R[2, 0] = 2 * (q[1] * q[3] + q[0] * q[2])
    R[2, 1] = 2 * (q[2] * q[3] - q[0] * q[1])
    R[2, 2] = 2 * q[0]**2 - 1 + 2 * q[3]**2
    
    return R