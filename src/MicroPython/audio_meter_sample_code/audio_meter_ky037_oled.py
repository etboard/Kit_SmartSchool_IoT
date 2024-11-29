from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import time
from OLED_U8G2 import oled_u8g2

# 상수 정의
THRESHOLD = 800         # 노이즈 임계값
MAX_LEVEL = 1000        # 최대 레벨값
SAMPLE_WINDOW = 1       # 샘플링 윈도우 (ms)
DISPLAY_INTERVAL = 200 # OLED 업데이트 간격 (ms)

# OLED 설정
oled = oled_u8g2()

# 사운드 센서 설정
sound_sensor = ADC(Pin(A6))
#sound_sensor.atten(ADC.ATTN_0DB)     # 더 작은 소리에 민감
#sound_sensor.atten(ADC.ATTN_2_5DB)  # 중간 낮은 범위
#sound_sensor.atten(ADC.ATTN_6DB)    # 중간 범위
sound_sensor.atten(ADC.ATTN_11DB)   # 큰 소리 범위 (기존)
sound_sensor.width(ADC.WIDTH_12BIT)

def get_sound_level():
    max_val = 0
    start_time = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start_time) < SAMPLE_WINDOW:
        val = sound_sensor.read()
        if val > max_val:
            max_val = val
    
    return max_val

def update_oled(current_value, max_value, count):
    oled.clear()
    oled.setLine(1, f"C: {current_value}")
    oled.setLine(2, f"M: {max_value}")
    oled.setLine(3, f"C: {count}")
    oled.display()

def main():
    count = 0
    last_display_time = time.ticks_ms()  # OLED 마지막 업데이트 시간
    max_raw_val = 0  # 표시 간격 동안의 최대값 저장
    
    while True:
        count = count + 1
        try:
            # 샘플링 수행
            raw_val = get_sound_level()
            
            # 현재 구간의 최대값 업데이트
            max_raw_val = max(max_raw_val, raw_val)
            
            # 현재 시간 확인
            current_time = time.ticks_ms()
            
            # DISPLAY_INTERVAL마다 OLED 업데이트
            if time.ticks_diff(current_time, last_display_time) >= DISPLAY_INTERVAL:                
                # OLED 업데이트
                update_oled(raw_val, max_raw_val, count)
                
                # 변수 초기화
                last_display_time = current_time
                max_raw_val = 0
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================