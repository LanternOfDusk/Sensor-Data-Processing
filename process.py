import requests
import json
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

# 서버 정보
MOBIUS_HOST = "203.253.128.177"
MOBIUS_PORT = 7579
MOBIUS_PATH = "/Mobius/LOD/MPU/la"

# HTTP 요청을 보내 데이터를 가져오는 함수
def fetch_data_from_server():
    url = f"http://{MOBIUS_HOST}:{MOBIUS_PORT}{MOBIUS_PATH}"
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 요청 실패 시 예외 발생
    data = response.json()
    return data

# 데이터 가져오기
data = fetch_data_from_server()

# JSON 데이터 파싱 (가정: 데이터는 gyroscope와 accelerometer 값을 포함)
def parse_data(data):
    content = json.loads(data['m2m:cin']['con'])
    gyr = np.array([
        [entry['GyroscopeX'], entry['GyroscopeY'], entry['GyroscopeZ']]
        for entry in content
    ])
    acc = np.array([
        [entry['AccelerometerX'], entry['AccelerometerY'], entry['AccelerometerZ']]
        for entry in content
    ])
    return gyr, acc

gyr, acc = parse_data(data)

# 샘플링 주기 설정
sample_period = 1/256

# MahonyAHRS 초기화
ahrs = MahonyAHRS(sample_period=sample_period, kp=1)

# 회전 행렬 계산
R = np.zeros((3, 3, len(gyr)))

for i in range(len(gyr)):
    ahrs.update_imu(gyr[i] * (np.pi/180), acc[i])
    R[:, :, i] = quatern2rotMat(ahrs.quaternion).T  # 센서 기준에서 지구 기준으로 변환

# '틸트 보정된' 가속도계 계산
tc_acc = np.zeros_like(acc)

for i in range(len(acc)):
    tc_acc[i, :] = R[:, :, i] @ acc[i, :]

# 지구 기준의 선형 가속도 계산 (중력 제거)
lin_acc = tc_acc - np.array([0, 0, 1])
lin_acc = lin_acc * 9.81  # 'g'에서 m/s^2로 변환

# 선형 속도 계산 (가속도 적분)
lin_vel = np.zeros_like(lin_acc)

for i in range(1, len(lin_acc)):
    lin_vel[i, :] = lin_vel[i-1, :] + lin_acc[i, :] * sample_period

# 선형 속도에 고역 통과 필터 적용하여 드리프트 제거
order = 1
filt_cutoff = 0.1
b, a = butter(order, (2 * filt_cutoff) / (1 / sample_period), 'high')
lin_vel_hp = filtfilt(b, a, lin_vel, axis=0)

# 선형 위치 계산 (속도 적분)
lin_pos = np.zeros_like(lin_vel_hp)

for i in range(1, len(lin_vel_hp)):
    lin_pos[i, :] = lin_pos[i-1, :] + lin_vel_hp[i, :] * sample_period

# 선형 위치에 고역 통과 필터 적용하여 드리프트 제거
lin_pos_hp = filtfilt(b, a, lin_pos, axis=0)

# 필요한 경우 lin_pos_hp를 반환하거나 저장할 수 있습니다
