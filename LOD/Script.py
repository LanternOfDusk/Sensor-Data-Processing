import sys
import os
import numpy as np
from scipy.signal import butter, filtfilt

# 경로 설정
current_directory = os.path.dirname(os.path.abspath(__file__))
ximu_library_path = os.path.join(current_directory, 'ximu_matlab_library')
quaternion_library_path = os.path.join(current_directory, 'quaternion_library')
mahony_ahrs_path = os.path.join(current_directory, 'MahonyAHRS')

sys.path.append(ximu_library_path)
sys.path.append(quaternion_library_path)
sys.path.append(mahony_ahrs_path)

# 필요한 클래스들 import
from xIMUdataClass import xIMUdataClass
from MahonyAHRS import MahonyAHRS
from quaternions import quatern2rotMat

# 데이터 가져오기
xIMUdata = xIMUdataClass('LoggedData/LoggedData')

samplePeriod = 1 / 100

gyr = np.array([xIMUdata.CalInertialAndMagneticData.Gyroscope.X,
                xIMUdata.CalInertialAndMagneticData.Gyroscope.Y,
                xIMUdata.CalInertialAndMagneticData.Gyroscope.Z]).T  # 자이로스코프 데이터

acc = np.array([xIMUdata.CalInertialAndMagneticData.Accelerometer.X,
                xIMUdata.CalInertialAndMagneticData.Accelerometer.Y,
                xIMUdata.CalInertialAndMagneticData.Accelerometer.Z]).T  # 가속도계 데이터

# AHRS 알고리즘을 통한 데이터 처리 (자세 계산)
R = np.zeros((3, 3, len(gyr)))  # 지구에 대한 센서의 회전 행렬

ahrs = MahonyAHRS(SamplePeriod=samplePeriod, Kp=1)

for i in range(len(gyr)):
    ahrs.UpdateIMU(gyr[i, :] * (np.pi / 180), acc[i, :])  # 자이로스코프 단위를 라디안으로 변환
    R[:, :, i] = quatern2rotMat(ahrs.Quaternion).T  # ahrs는 지구에 대한 센서를 제공하므로 전치

# '틸트 보정' 가속도계 계산
tcAcc = np.zeros(acc.shape)  # 지구 프레임의 가속도계

for i in range(len(acc)):
    tcAcc[i, :] = np.dot(R[:, :, i], acc[i, :])

# 지구 프레임에서 선형 가속도 계산 (중력 제거)
linAcc = tcAcc - np.array([np.zeros(len(tcAcc)), np.zeros(len(tcAcc)), np.ones(len(tcAcc))]).T
linAcc = linAcc * 9.81  # 'g'에서 m/s^2로 변환

# 선형 속도 계산 (가속도 적분)
linVel = np.zeros(linAcc.shape)

for i in range(1, len(linAcc)):
    linVel[i, :] = linVel[i - 1, :] + linAcc[i, :] * samplePeriod

# 드리프트를 제거하기 위해 고역통과 필터 적용
order = 1
filtCutOff = 0.1
b, a = butter(order, (2 * filtCutOff) / (1 / samplePeriod), 'high')
linVelHP = filtfilt(b, a, linVel, axis=0)

# 선형 위치 계산 (속도 적분)
linPos = np.zeros(linVelHP.shape)

for i in range(1, len(linVelHP)):
    linPos[i, :] = linPos[i - 1, :] + linVelHP[i, :] * samplePeriod

# 드리프트를 제거하기 위해 고역통과 필터 적용
linPosHP = filtfilt(b, a, linPos, axis=0)

for i in range(len(linPosHP)):
    print(f"High-pass filtered position at sample {i}: X={linPosHP[i, 0]}, Y={linPosHP[i, 1]}, Z={linPosHP[i, 2]}")
# 위치와 회전행렬을 애니메이션에 사용하도록 준비 (시각화는 제거)
SamplePlotFreq = 8

# 필수 클래스와 함수들이 있는 모듈들을 가져온 후, 필터링된 위치 및 회전 행렬을 사용하여 애니메이션 생성
# animation = SixDOFanimation(linPosHP, R, SamplePlotFreq=SamplePlotFreq, ...)
