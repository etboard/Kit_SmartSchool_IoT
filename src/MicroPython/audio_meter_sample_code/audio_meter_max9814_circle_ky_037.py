from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import neopixel
import time
import ssd1306

# OLED 설정
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 센서 및 네오픽셀 설정
sound_sensor = ADC(Pin(A3))
sound_sensor.atten(ADC.ATTN_11DB)
sound_sensor.width(ADC.WIDTH_12BIT)

NUM_PIXELS = 12
pixels = neopixel.NeoPixel(Pin(D2), NUM_PIXELS)

# 색상 정의 (낮은 밝기)
GREEN = (0, 15, 0)     # 초록색
YELLOW = (15, 15, 0)   # 노란색
RED = (15, 0, 0)       # 빨간색

# 레벨 설정
THRESHOLD = 1600       # 노이즈 임계값
MAX_LEVEL = 2300       # 최대 레벨값 증가

# LED 설정
DECAY_RATE = 0.85      # 감소율 (0.85 = 85% 유지)
LED_UPDATE_INTERVAL = 100  # LED 업데이트 주기 (ms)

# 샘플링 설정
SAMPLE_WINDOW = 2      # 샘플링 윈도우 (ms)

# LED 색상 배열
LED_COLORS = [GREEN, GREEN, GREEN, GREEN,     # 4개의 초록색
              YELLOW, YELLOW, YELLOW, YELLOW,  # 4개의 노란색
              RED, RED, RED, RED]             # 4개의 빨간색

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

def update_oled(current_value):
    # OLED 디스플레이 업데이트
    oled.fill(0)
    oled.text("Sound Level:", 0, 0)
    oled.text(str(current_value), 0, 10)
    oled.show()

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
            if time.ticks_diff(current_time, last_led_update) >= LED_UPDATE_INTERVAL:
                update_leds(current_value)
                #update_oled(current_value)
                
                # 값 감소 (더 천천히)
                current_value = int(current_value * DECAY_RATE)
                
                # 업데이트 시간 기록
                last_led_update = current_time
            
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