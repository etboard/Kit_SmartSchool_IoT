# MAX9814 사운드 미터 - ETboard용 코드 설명

## 원본 코드 분석

원본 코드는 일반적인 아날로그 사운드 센서나 마이크를 위한 것으로, MAX9814 모듈에 특화되지 않았습니다.

### 주요 특징:
- ADC를 통해 아날로그 신호를 직접 읽음
- 진폭의 최대값과 최소값으로 단순하게 주파수 추정
- OLED 디스플레이에 진폭과 추정 주파수 시각화

## MAX9814를 위한 코드 수정

MAX9814 모듈에 더 적합하도록 코드를 수정했습니다.

### 주요 변경 사항:
1. 샘플링 레이트와 샘플 수 명시적 정의 (10kHz)
2. `get_sound_samples()` 함수 수정 - 정확한 시간 간격으로 샘플 수집
3. RMS(Root Mean Square) 값 계산 함수 추가
4. 주파수 추정 방법을 영점 교차 방식으로 변경
5. OLED 디스플레이에 RMS 값과 추정 주파수 표시

## 수정된 코드

```python
from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import ssd1306
import utime
import math

# ADC 설정
adc = ADC(Pin(A3))
adc.atten(ADC.ATTN_11DB)

# OLED 설정
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
utime.sleep_ms(100)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 상수 정의
SAMPLE_RATE = 10000  # 10kHz
NUM_SAMPLES = 1000
SAMPLE_PERIOD_US = 1000000 // SAMPLE_RATE

def get_sound_samples():
    samples = []
    start_time = utime.ticks_us()
    for _ in range(NUM_SAMPLES):
        samples.append(adc.read())
        while utime.ticks_diff(utime.ticks_us(), start_time) < SAMPLE_PERIOD_US:
            pass
        start_time = utime.ticks_us()
    return samples

def calculate_rms(samples):
    return math.sqrt(sum(x*x for x in samples) / len(samples))

def estimate_frequency(samples):
    zero_crossings = 0
    for i in range(1, len(samples)):
        if (samples[i-1] < 2048 and samples[i] >= 2048) or (samples[i-1] >= 2048 and samples[i] < 2048):
            zero_crossings += 1
    return (zero_crossings * SAMPLE_RATE) / (2 * NUM_SAMPLES)

def draw_meter(value, max_value, y_pos, label):
    bar_width = int((value / max_value) * 100)
    oled.fill_rect(0, y_pos, bar_width, 10, 1)
    oled.text(f"{label}: {value:.2f}", 0, y_pos + 12, 1)

def main():
    while True:
        samples = get_sound_samples()
        rms = calculate_rms(samples)
        frequency = estimate_frequency(samples)

        oled.fill(0)  # Clear the display
        draw_meter(rms, 4095, 0, "RMS")
        draw_meter(frequency, 2000, 30, "Freq")
        oled.show()

        utime.sleep_ms(100)

if __name__ == "__main__":
    main()
```

## 추가 개선 사항

1. FFT(고속 푸리에 변환) 구현으로 더 정확한 주파수 분석
2. MAX9814의 게인 제어 핀 활용
3. 노이즈 필터링 추가

이 코드를 ETboard에서 실행해보시고, 필요한 경우 추가적인 조정이나 개선 사항에 대해 말씀해 주시면 더 도와드리겠습니다.
