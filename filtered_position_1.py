import requests
import numpy as np
from scipy.signal import butter, filtfilt

class MahonyAHRS:
    def __init__(self, SamplePeriod=1/256, Quaternion=np.array([1, 0, 0, 0], dtype=np.float64), Kp=1, Ki=0):
        self.SamplePeriod = SamplePeriod
        self.Quaternion = Quaternion
        self.Kp = Kp
        self.Ki = Ki
        self.eInt = np.array([0, 0, 0], dtype=np.float64)

    def update(self, Gyroscope, Accelerometer, Magnetometer=None):
        q = self.Quaternion.copy()

        # Normalise accelerometer measurement
        if np.linalg.norm(Accelerometer) == 0:
            return
        Accelerometer /= np.linalg.norm(Accelerometer)

        # Normalise magnetometer measurement if provided
        if Magnetometer is not None:
            if np.linalg.norm(Magnetometer) == 0:
                return
            Magnetometer /= np.linalg.norm(Magnetometer)
            # Reference direction of Earth's magnetic field
            h = self.quaternion_product(q, self.quaternion_product([0, Magnetometer[0], Magnetometer[1], Magnetometer[2]], self.quaternion_conjugate(q)))
            b = [0, np.linalg.norm([h[1], h[2]]), 0, h[3]]

        # Estimated direction of gravity
        v = [2*(q[1]*q[3] - q[0]*q[2]),
             2*(q[0]*q[1] + q[2]*q[3]),
             q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2]

        # Error is sum of cross product between estimated direction and measured direction of fields
        e = np.cross(Accelerometer, v)
        if self.Ki > 0:
            self.eInt += e * self.SamplePeriod

        # Apply feedback terms
        Gyroscope += self.Kp * e + self.Ki * self.eInt

        # Compute rate of change of quaternion
        qDot = 0.5 * self.quaternion_product(q, [0, Gyroscope[0], Gyroscope[1], Gyroscope[2]])

        # Integrate to yield quaternion
        q += qDot * self.SamplePeriod
        self.Quaternion = q / np.linalg.norm(q)

    def update_IMU(self, Gyroscope, Accelerometer):
        q = self.Quaternion.copy()

        # Normalise accelerometer measurement
        if np.linalg.norm(Accelerometer) == 0:
            return
        Accelerometer /= np.linalg.norm(Accelerometer)

        # Estimated direction of gravity
        v = [2*(q[1]*q[3] - q[0]*q[2]),
             2*(q[0]*q[1] + q[2]*q[3]),
             q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2]

        # Error is sum of cross product between estimated direction and measured direction of field
        e = np.cross(Accelerometer, v)
        if self.Ki > 0:
            self.eInt += e * self.SamplePeriod

        # Apply feedback terms
        Gyroscope += self.Kp * e + self.Ki * self.eInt

        # Compute rate of change of quaternion
        qDot = 0.5 * self.quaternion_product(q, [0, Gyroscope[0], Gyroscope[1], Gyroscope[2]])

        # Integrate to yield quaternion
        q += qDot * self.SamplePeriod
        self.Quaternion = q / np.linalg.norm(q)

    @staticmethod
    def quaternion_product(q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return [w1*w2 - x1*x2 - y1*y2 - z1*z2,
                w1*x2 + x1*w2 + y1*z2 - z1*y2,
                w1*y2 - x1*z2 + y1*w2 + z1*x2,
                w1*z2 + x1*y2 - y1*x2 + z1*w2]

    @staticmethod
    def quaternion_conjugate(q):
        w, x, y, z = q
        return [w, -x, -y, -z]

# MOBIUS 서버 정보 정의
MOBIUS_HOST = "203.253.128.177"
MOBIUS_PORT = 7579
MOBIUS_PATH = "/Mobius/LOD/MPU"

# MOBIUS 서버에서 데이터 가져오기
response = requests.get(f"http://{MOBIUS_HOST}:{MOBIUS_PORT}{MOBIUS_PATH}")
data = response.json()

# gyro와 accel 값을 추출하여 리스트로 저장
gyro_values = np.array(data['Gyroscope'])
accel_values = np.array(data['Accelerometer'])

# 샘플 주기
sample_period = 1 / 256

# AHRS 객체 생성
ahrs = MahonyAHRS(SamplePeriod=sample_period)

# 선형 가속도 및 각속도 계산
linAcc = np.zeros_like(accel_values)  # 수정된 부분
linVel = np.zeros_like(gyro_values)  # 수정된 부분

for i in range(len(gyro_values)):
    # AHRS 알고리즘 업데이트
    ahrs.update(gyro_values[i], accel_values[i])  # 수정된 부분

    # '틸트 보정된' 가속도계 계산
    tcAcc = ahrs.Quaternion * accel_values[i] * ahrs.quaternion_conjugate(ahrs.Quaternion)  # 수정된 부분

    # 지구 프레임에서 선형 가속도 계산
    linAcc[i] = tcAcc - np.array([0, 0, 1])

    # 선형 속도 계산
    if i > 0:
        linVel[i] = linVel[i - 1] + linAcc[i] * sample_period

# 드리프트 제거를 위해 선형 속도에 하이패스 필터 적용
order = 1
filter_cutoff = 0.1
b, a = butter(order, (2 * filter_cutoff) / (1/sample_period), 'high')

# 입력 벡터의 길이가 필터 계수보다 작을 때 패딩 적용
pad_length = max(len(b), len(a)) - 1  # 패딩 길이를 조정
if len(linVel) < pad_length:
    linVel_padded = np.pad(linVel, (0, pad_length), mode='edge')
else:
    linVel_padded = linVel

linVelHP = filtfilt(b, a, linVel_padded)

# 선형 위치 계산
linPos = np.zeros_like(gyro_values)  # 수정된 부분

for i in range(1, len(linVelHP)):
    linPos[i] = linPos[i - 1] + linVelHP[i] * sample_period

# 드리프트 제거를 위해 선형 위치에 하이패스 필터 적용
order = 1
filter_cutoff = 0.1
b, a = butter(order, (2 * filter_cutoff) / (1/sample_period), 'high')
linPosHP = filtfilt(b, a, linPos)

# 선형 위치 출력
print("선형 위치 (하이패스 필터링 적용):")
print(linPosHP)
