import sys
import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

# 업로드된 파일 경로 설정
#ximu_library_path = '/LOD/ximu_matlab_library/xIMUdataClass.py'
#quaternion_library_path = '/LOD/quaternion_library/quatern2rotMat.py'
#mahony_ahrs_path = '/LOD/MahonyAHRS/MahonyAHRS.py'
#logged_data_path = '/LOD/LoggedData/LoggedData_CalInertialAndMag.csv'
current_directory = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(ximu_library_path))
#sys.path.append(os.path.dirname(quaternion_library_path))
#sys.path.append(os.path.dirname(mahony_ahrs_path))

# 필요한 클래스들 import
from xIMUdataClass import xIMUdataClass
from MahonyAHRS import MahonyAHRS
from quatern2rotMat import quatern2rotMat

# 데이터 가져오기
# xIMUdata = xIMUdataClass('LoggedData/LoggedData') 대신 CSV 파일 로드
logged_data_path = os.path.join(current_directory, 'LoggedData_CalInertialAndMag.csv')
data = pd.read_csv(logged_data_path)

# 자이로스코프 데이터 (deg/s 단위)
gyr = np.array([data['Gyroscope X (deg/s)'], data['Gyroscope Y (deg/s)'], data['Gyroscope Z (deg/s)']]).T

# 가속도계 데이터 (g 단위)
acc = np.array([data['Accelerometer X (g)'], data['Accelerometer Y (g)'], data['Accelerometer Z (g)']]).T

samplePeriod = 1 / 100

# AHRS 알고리즘을 통한 데이터 처리 (자세 계산)
R = np.zeros((3, 3, len(gyr)))  # 지구에 대한 센서의 회전 행렬

ahrs = MahonyAHRS(SamplePeriod=samplePeriod, Kp=1)

for i in range(len(gyr)):
    ahrs.updateIMU(gyr[i, :] * (np.pi / 180), acc[i, :])  # 자이로스코프 단위를 라디안으로 변환
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
