#******************************************************************************************
# FileName     : SmartNosieCheck_Basic.py
# Description  : 스마트 소음 측정 코딩 키트
# Author       : 손철수
# Created Date : 2024.11.25 : 손철수 : 최초작성
# Reference    : 
# Modified     : 2024.11.29 : 박은정 : 코드 구조 변경, 주석 추가, 파일명 변경
# Modified     : 2024.11.29 : 박은정 : OLED 표시 변경
# ******************************************************************************************


#===========================================================================================
# 기본 모듈 사용하기
#===========================================================================================
import neopixel
import time
from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
from OLED_U8G2 import oled_u8g2
from ETboard.lib.servo import Servo


#===========================================================================================
# 전역 변수 선언
#===========================================================================================
oled = oled_u8g2()                                       # OLED 초기화

sound_sensor = ADC(Pin(A6))                              # 사운드 센서 핀: A6
sound_sensor.atten(ADC.ATTN_11DB)                        # ADC 입력 전압 범위를 3.3V로 설정
sound_sensor.width(ADC.WIDTH_12BIT)                      # ADC 해상도를 12비트로 설정

NUM_PIXELS = 4                                           # 네오픽셀 LED 개수 설정
pixels = neopixel.NeoPixel(Pin(D2), NUM_PIXELS)          # 네오픽셀 핀: D2, 네오픽셀 초기화

servo = Servo(Pin(D6))                                   # 서보모터 핀: D6

# 소리를 얼마나 작게 들리거나 크게 들리는지 정하는 기준, 소음 센서에 따라 수정
# THRESHOLD: '이 정도면 소리가 들린다'고 판단하는 최소 값
# MAX_LEVEL: '이 이상이면 소리가 너무 크다'고 판단하는 값
THRESHOLD = 1500                                         # 소리가 들린다고 느끼는 최소 값
MAX_LEVEL = 1800                                         # 소리가 가장 큰 값을 정한 것

UPDATE_INTERVAL = 200                                    # LED 업데이트 주기 (밀리초)
DECAY_RATE = 0.85                                        # 감소율 (85%)

GREEN = (0, 64, 0)                                       # 초록색 (적절한 소음)
YELLOW = (64, 64, 0)                                     # 노란색 (적당한 소음)
RED = (64, 0, 0)                                         # 빨간색 (매우 큰 소음)

SAMPLE_WINDOW = 1                                        # 소음 측정 주기(ms)

LED_COLORS = [GREEN, YELLOW, YELLOW, RED]                # LED 색상 배열


#===========================================================================================
def setup():                                             # 설정 함수
#===========================================================================================
    global current_value, last_led_update
    current_value = 0
    last_led_update = time.ticks_ms()
    
    pixels.fill((0, 0, 0))
    pixels.write()


#===========================================================================================
def loop():                                              # 반복 함수
#===========================================================================================
    global current_value, last_led_update

    try:
        val = get_sound_level()                          # 소음 측정 함수 호출

        if val > THRESHOLD:                              # 측정 값이 기준치보다 클 때
            level = val - THRESHOLD                      # 기준치에서 초과된 값 계산
            if level > current_value:                    # 현재 소음 값 업데이트
                current_value = level

        noise_status = classify_sound_level(current_value)      # 소음 크기 분류
            
        current_time = time.ticks_ms()                   # 현재 시간 가져오기
            
        if time.ticks_diff(current_time, last_led_update) >= UPDATE_INTERVAL:
            update_leds(current_value)                   # LED 상태 업데이트
                
            angle = compute_angle(current_value)         # 서보모터 각도 계산
            servo.write_angle(angle)                     # 서보모터 제어
                
            update_oled(current_value, noise_status)     # OLED 디스플레이 업데이트
                
            current_value = int(current_value * DECAY_RATE)     # 소음 값 감소
                
            last_led_update = current_time               # 마지막 업데이트 시간 기록
            
    except Exception as e:                               # 오류 처리
        print(f"Error: {e}")
        pixels.fill((0, 0, 0))                           # 오류 발생 시 모든 LED 끄기
        pixels.write()


#===========================================================================================
def get_sound_level():                                   # 소리 측정
#===========================================================================================
    max_val = 0                                          # 최대 소음 값 초기화
    start_time = time.ticks_ms()                         # 샘플링 시작 시간 기록

    while time.ticks_diff(time.ticks_ms(), start_time) < SAMPLE_WINDOW:
        val = sound_sensor.read()                        # 소음 센서 값 읽기
        if val > max_val:                                # 최대 값 업데이트
            max_val = val

    return max_val                                       # 측정된 최대 소음 값 반환

#===========================================================================================
def classify_sound_level(current_value):                 # 소리 단계 분류
#===========================================================================================
    if current_value < 1400:
        return "Whisper"                                 # 소리가 작음
    elif current_value < 1700:
        return "Racket"                                  # 중간 크기 소음
    else:
        return "Clamor"                                  # 소리가 큼


#===========================================================================================
def update_leds(current_value):                          # 네오픽셀 업데이트
#===========================================================================================
    num_leds = (current_value * NUM_PIXELS) // MAX_LEVEL # 켜질 LED 개수 계산
    num_leds = min(num_leds, NUM_PIXELS)                 # LED 개수 제한

    pixels.fill((0, 0, 0))                               # 모든 LED 끄기
    for i in range(num_leds):                            # 켜질 LED에 색상 설정
        pixels[i] = LED_COLORS[i]
    pixels.write()                                       # LED 상태 업데이트


#===========================================================================================
def update_oled(current_value, noise_status):            # OLED 업데이트
#===========================================================================================
    oled.clear()                                         # OLED 화면 지우기
    oled.setLine(1, "ETboard")                           # 첫 번째 줄: 보드 이름 표시
    oled.setLine(2, f"Noise: {current_value}")           # 두 번째 줄: 소음 값 표시
    oled.setLine(3, noise_status)                        # 세 번째 줄: 소음 상태 표시
    oled.display()                                       # OLED 화면 업데이트


#===========================================================================================
def compute_angle(current_value):                        # 서보모터 제어
#===========================================================================================
    if current_value < THRESHOLD:                        # 소음이 기준치보다 작으면
        return 180                                       # 서보모터를 180도로 유지

    level = min(current_value, MAX_LEVEL)                # 소음 값 제한 (최대값)
    level = max(level, THRESHOLD)                        # 소음 값 제한 (최소값)

    angle = 180 - (level - THRESHOLD) * 180 / (MAX_LEVEL - THRESHOLD)
    angle = max(0, min(180, angle))                      # 각도를 0도~180도 사이로 제한

    return int(angle)                                    # 계산된 각도 반환


#===========================================================================================
# start point
#===========================================================================================
if __name__ == "__main__":
    setup()
    while True:
        loop()


#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================
