#******************************************************************************************
# FileName     : audio_meter_ky037_neopixcel_oled_servo.py
# Description  : 사운드 미터
# Author       : 손철수
# Created Date : 2024.11.25 : 손철수 : 최초작성
# Reference    : 
# Modified     : 
# ******************************************************************************************

from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import neopixel
import time
from OLED_U8G2 import oled_u8g2
from ETboard.lib.servo import Servo

# 레벨 설정
THRESHOLD = 2000       # 노이즈 임계값
MAX_LEVEL = 2300       # 최대 레벨값 증가
THRESHOLD = 1900       # 노이즈 임계값
MAX_LEVEL = 2100       # 최대 레벨값 증가

# 표시 설정
UPDATE_INTERVAL = 200  # LED 업데이트 주기 (ms)
DECAY_RATE = 0.85      # 감소율 (0.85 = 85% 유지)


# OLED 설정
oled = oled_u8g2()

# 사운드 센서
sound_sensor = ADC(Pin(A6))
sound_sensor.atten(ADC.ATTN_11DB)
sound_sensor.width(ADC.WIDTH_12BIT)

# 네오픽셀 설정
NUM_PIXELS = 4
pixels = neopixel.NeoPixel(Pin(D2), NUM_PIXELS)

# 서보 모터
servo = Servo(Pin(D6))                          # 서보모터 핀 지정

# 색상 정의 (낮은 밝기)
GREEN = (0, 64, 0)     # 초록색
YELLOW = (64, 64, 0)   # 노란색
RED = (64, 0, 0)       # 빨간색

# 샘플링 설정
SAMPLE_WINDOW = 1      # 샘플링 윈도우 (ms)

# LED 색상 배열
LED_COLORS = [GREEN, YELLOW, YELLOW, RED]       # 4개의 색

def get_sound_level():
    # 짧은 시간 동안 최대한 많은 샘플링
    max_val = 0
    start_time = time.ticks_ms()
    
    # SAMPLE_WINDOW 시간 동안 계속 샘플링
    while time.ticks_diff(time.ticks_ms(), start_time) < SAMPLE_WINDOW:
        val = sound_sensor.read()
        if val > max_val:
            max_val = val
        
    return max_val

def update_leds(current_value):
    # LED 개수 계산
    num_leds = (current_value * NUM_PIXELS) // MAX_LEVEL
    num_leds = min(num_leds, NUM_PIXELS)
    
    # LED 업데이트
    pixels.fill((0, 0, 0))
    for i in range(num_leds):
        pixels[i] = LED_COLORS[i]
    pixels.write()

def update_oled(current_value, angle_value):
    oled.clear()
    oled.setLine(2, str(current_value))
    oled.setLine(3, str(angle_value))
    oled.display()
    
def compute_angle(current_value):
    # 소리 레벨을 180도에서 0도 사이의 값으로 매핑
    # 소리가 커질수록 부드럽게 180° → 0° 방향으로 이동
    
    if current_value < THRESHOLD:
        return 180  # 임계값 이하일 때는 180도 유지
    
    # 소리 레벨을 서보모터 각도로 선형 매핑
    # current_value: THRESHOLD ~ MAX_LEVEL
    # angle: 180° ~ 0°
    
    # 소리 레벨 범위 제한
    level = min(current_value, MAX_LEVEL)
    level = max(level, THRESHOLD)
    
    # 선형 매핑 공식: (입력값 - 입력최소) * (출력범위) / (입력범위) + 출력최소
    angle = 180 - (level - THRESHOLD) * 180 / (MAX_LEVEL - THRESHOLD)
    
    # 각도 범위 보장
    angle = max(0, min(180, angle))
    
    return int(angle)  # 정수로 변환
    

def main():
    current_value = 0
    last_led_update = time.ticks_ms()
    
    pixels.fill((0, 0, 0))
    pixels.write()
    
    while True:
        try:
            # 샘플링 수행
            val = get_sound_level()
            
            # 임계값 이상일 때만 처리
            if val > THRESHOLD:
                level = val - THRESHOLD
                if level > current_value:
                    current_value = level
            
            # 현재 시간 확인
            current_time = time.ticks_ms()
            
            # LED 업데이트 주기가 되었을 때만 LED 업데이트
            if time.ticks_diff(current_time, last_led_update) >= UPDATE_INTERVAL:
                # LED 업데이트
                update_leds(current_value)
                
                # 서보모터 각도 계산 및 제어
                angle = compute_angle(current_value)                
                servo.write_angle(angle)
                
                # OLED 업데이트
                update_oled(current_value, angle)
                
                # 값 감소 (더 천천히)
                current_value = int(current_value * DECAY_RATE)
                
                # 업데이트 시간 기록
                last_led_update = current_time
                
                #time.sleep(0.001)                
            
        except Exception as e:
            print(f"Error: {e}")
            pixels.fill((0, 0, 0))
            pixels.write()

if __name__ == "__main__":
    try:
        main()
    finally:
        pixels.fill((0, 0, 0))
        pixels.write()

#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================
