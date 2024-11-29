from ETboard.lib.pin_define import *
from machine import ADC, Pin, I2C
import ssd1306
import utime
import math
from machine import ADC, Pin
from time import sleep

sound_pin = ADC(A6)
sound_pin.atten(ADC.ATTN_11DB)
sound_pin.width(ADC.WIDTH_12BIT)

quiet_threshold = 100 + 200
medium_threshold = quiet_threshold + 300
loud_threshold = medium_threshold + 300

def get_average_level():
   samples = []
   start_time = utime.ticks_ms()
   
   while utime.ticks_diff(utime.ticks_ms(), start_time) < 1:
       #samples.append(sound_pin.read_u16())
       samples.append(sound_pin.read())
   
   cnt = len(samples)
   avg = sum(samples) / cnt
   
   if avg < quiet_threshold:
       return "Level 1:", quiet_threshold, avg, cnt
   elif avg < medium_threshold:
       return "Level 2:", medium_threshold, avg, cnt
   else:
       return "Level 3:", loud_threshold, avg, cnt

while True:
   level, threshold, value, cnt = get_average_level()
   #print(level, (threshold-value), threshold, value)
   difference = threshold - value
   print(f"Level {level}: count:{cnt} {difference:>6.1f} {threshold:>6} {value:>8.1f}")
   sleep(0.1)