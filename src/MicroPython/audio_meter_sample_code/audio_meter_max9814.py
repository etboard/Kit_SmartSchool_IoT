#******************************************************************************************
# FileName     : audio_meter_max9814.py
# Description  : MAX9814르 이용한 사운드 미터
# Author       : 손철수
# Created Date : 2024.09.25 : 손철수 : 최초작성
# Reference    : MAX9814 사운드 센서는 A3에 연결됨
# Modified     : 
# ******************************************************************************************

from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import ssd1306
import utime
import math

# ADC 설정
adc = ADC(Pin(A3))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

# OLED 설정
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
utime.sleep_ms(100)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 상수 정의
SAMPLE_WINDOW = 50  # ms
SAMPLE_RATE = 10000  # Hz
NUM_SAMPLES = SAMPLE_WINDOW * SAMPLE_RATE // 1000

def get_sound_samples():
    samples = []
    start_time = utime.ticks_us()
    for _ in range(NUM_SAMPLES):
        samples.append(adc.read())
        while utime.ticks_diff(utime.ticks_us(), start_time) < 100:  # 100us 간격으로 샘플링
            pass
        start_time = utime.ticks_us()
    return samples

def calculate_rms(samples):
    return math.sqrt(sum([s*s for s in samples]) / len(samples))

def estimate_frequency(samples):
    # 간단한 영점 교차 방식으로 주파수 추정
    zero_crossings = 0
    prev_sample = samples[0]
    for sample in samples[1:]:
        if (prev_sample < 2048 and sample >= 2048) or (prev_sample >= 2048 and sample < 2048):
            zero_crossings += 1
        prev_sample = sample
    return zero_crossings * SAMPLE_RATE / (2 * NUM_SAMPLES)

def draw_meter(value, max_value, y_pos, label):
    bar_width = int((value / max_value) * 100)
    oled.fill_rect(0, y_pos, bar_width, 10, 1)
    oled.text(f"{label}: {value:.0f}", 0, y_pos + 12, 1)

def main():
    while True:
        samples = get_sound_samples()
        rms = calculate_rms(samples)
        frequency = estimate_frequency(samples)

        oled.fill(0)  # Clear the display
        
        # Draw RMS amplitude meter
        draw_meter(rms, 4095, 0, "RMS")
        
        # Draw frequency meter
        draw_meter(frequency, 2000, 30, "Freq")
        
        # Display additional info
        oled.text(f"Samples: {len(samples)}", 0, 54, 1)
        
        oled.show()
        utime.sleep_ms(100)

if __name__ == "__main__":
    main()

    
#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================
