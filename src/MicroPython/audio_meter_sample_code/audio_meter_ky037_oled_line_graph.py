#******************************************************************************************
# FileName     : sound_level_monitor.py
# Description  : KY-037을 이용한 소리 크기 모니터링
# Author       : 손철수
# Created Date : 2024.09.25 : 손철수 : 최초작성
# Reference    : KY-037 사운드 센서는 A3에 연결됨
# Modified     : 2024.11.11 : Changed to line graph
#******************************************************************************************
from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import ssd1306
import utime
import math

# ADC 설정 (KY-037 아날로그 출력 핀)
adc = ADC(Pin(A3))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

# OLED 설정
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=1000000)
utime.sleep_ms(100)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 상수 정의
SAMPLE_WINDOW = 50  # ms
SAMPLE_RATE = 10000  # Hz
NUM_SAMPLES = SAMPLE_WINDOW * SAMPLE_RATE // 1000
HISTORY_SIZE = 16  # 그래프에 표시할 이전 측정값 개수

# 측정값 히스토리 저장용 리스트
level_history = [0] * HISTORY_SIZE

def get_sound_level():
    max_value = 0
    min_value = 4095
    
    start_time = utime.ticks_us()
    for _ in range(NUM_SAMPLES):
        value = adc.read()
        if value > max_value:
            max_value = value
        if value < min_value:
            min_value = value
            
        while utime.ticks_diff(utime.ticks_us(), start_time) < 100:  # 100us 간격으로 샘플링
            pass
        start_time = utime.ticks_us()
    
    # 피크-투-피크 값 반환
    return max_value - min_value

def get_level_text(value):
    """상대적인 소리 크기 수준을 반환"""
    if value < 100:
        return "QUIET"
    elif value < 300:
        return "NORMAL"
    elif value < 500:
        return "LOUD"
    else:
        return "V.LOUD"

def draw_line_graph(values, min_value, max_value):
    # 그래프 영역 설정
    GRAPH_HEIGHT = 40
    GRAPH_BOTTOM = 60
    LABEL_WIDTH = 30  # Y축 레이블을 위한 공간
    GRAPH_WIDTH = 128 - LABEL_WIDTH - 5  # 그래프 영역 너비
    
    # Y축 눈금 표시 (200 단위로, 5개 구간)
    Y_TICKS = [0, 200, 400, 600, 800]
    Y_SPACING = GRAPH_HEIGHT / (len(Y_TICKS) - 1)  # 눈금 간격 계산
    
    # Y축 눈금과 레이블 그리기
    for i, value in enumerate(Y_TICKS):
        y = int(GRAPH_BOTTOM - (i * Y_SPACING))
        oled.pixel(LABEL_WIDTH, y, 1)  # 눈금 표시
        if value > 0:  # 0은 X축과 겹치므로 생략
            oled.text(str(value), 1, y-4, 1)  # 레이블 표시
    
    # 점들의 위치 계산
    points = []
    x_spacing = GRAPH_WIDTH / (len(values) - 1)
    for i, value in enumerate(values):
        x = int(LABEL_WIDTH + (i * x_spacing))
        normalized_height = (value - min_value) / (max_value - min_value)
        y = int(GRAPH_BOTTOM - (normalized_height * GRAPH_HEIGHT))
        points.append((x, y))
    
    # 선 그리기
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        oled.line(x1, y1, x2, y2, 1)
    
    # 데이터 포인트 표시
    for x, y in points:
        oled.fill_rect(x-1, y-1, 3, 3, 1)  # 작은 사각형으로 포인트 표시
    
    # X축 그리기
    oled.hline(LABEL_WIDTH, GRAPH_BOTTOM, GRAPH_WIDTH, 1)
    
    # Y축 그리기
    oled.vline(LABEL_WIDTH, GRAPH_BOTTOM - GRAPH_HEIGHT, GRAPH_HEIGHT, 1)
    
    # 현재 값과 상태 표시
    current_value = values[-1]
    level_text = get_level_text(current_value)
    value_str = f"Lv:{int(current_value)}"
    oled.text(value_str, 2, 2, 1)
    oled.text(level_text, 75, 2, 1)

def main():
    while True:
        try:
            level = get_sound_level()
            
            # 히스토리 업데이트
            level_history.pop(0)
            level_history.append(level)
            
            oled.fill(0)
            
            # 꺾은선 그래프 그리기
            draw_line_graph(level_history, 0, 800)
            
            oled.show()
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================