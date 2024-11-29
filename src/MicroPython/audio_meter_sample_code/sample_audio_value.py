from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import neopixel
import time
from OLED_U8G2 import oled_u8g2
from ETboard.lib.servo import Servo

sound_sensor = ADC(A6)
sound_sensor.atten(ADC.ATTN_6DB)
#sound_sensor.atten(ADC.ATTN_11DB)
sound_sensor.width(ADC.WIDTH_12BIT)

# 샘플링 설정
SAMPLE_WINDOW = 10      # 샘플링 윈도우 (ms)

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

count = 0
while True:
    count = count + 1    
    val = get_sound_level()
    #print(f"count:{count}, val:{val}")
    if (val > 100):
        print(f"count:{count}, val:{val}")
        time.sleep(0.1)
    #else:
        #time.sleep(0.001)