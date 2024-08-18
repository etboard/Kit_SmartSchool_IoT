# ******************************************************************************************
# FileName     : Kit_SmartSchool_IoT.py
# Description  : 
# Author       : 손철수
# Created Date : 2024.08.18 : 손철수 : 최소
# Reference    :
# Modified     : 
# ******************************************************************************************
from machine import Pin
from ETboard.lib.pin_define import *              # ETboard 핀 관련 모듈

count = 0

#===========================================================================================
# IoT 프로그램 사용하기                       
#===========================================================================================
from ET_IoT_App import ET_IoT_App, setup, loop
app = ET_IoT_App()


#===========================================================================================
# DHT 온도 센서 사용하시
#===========================================================================================
from ET_DHTSensor import ET_DHTSensor            # 온습도 센서
dht_sensor = ET_DHTSensor(D9)                    # 9번 핀에 연


#===========================================================================================
# 미세먼지 센서 사용하기
#===========================================================================================
from ET_PPD42NS import ET_PPD42NS                 # 미세먼지 센서
dust_sensor = ET_PPD42NS(A4);                     # A4 핀에 센서 연결


#===========================================================================================
# 사운드 센서 사용하기
#===========================================================================================
from ET_MAX9814 import ET_MAX9814                  # 사운드센서
sound_sensor = ET_MAX9814(A3);                     # A3번에 센서 연결


#===========================================================================================
# OLED 표시 장치 사용하기
#===========================================================================================
from ETboard.lib.OLED_U8G2 import *
oled = oled_u8g2()


#===========================================================================================
# 응용 프로그램 설정하기(1회만 실행)
#===========================================================================================
def et_setup():
    app.setup_recv_message("none", recv_message)
    dust_sensor.begin()
    

#===========================================================================================
# 응용 프로그램 루프(반복 시행)
#===========================================================================================
def et_loop():
    do_sensing()


#===========================================================================================
# 센싱 처리                     
#===========================================================================================
def do_sensing():
    global count    
    count = count + 1
    dht_sensor.update()
    dust_sensor.update()
    sound_sensor.update()


#===========================================================================================
# 짭은 주기 처리                    
#===========================================================================================
def et_short_periodic_process():    
    display_information()
    

#===========================================================================================
# 긴 주기 처리                
#===========================================================================================
def et_long_periodic_process():    
    send_message()
    sound_sensor.reset()
    

#===========================================================================================
# 정보 표시               
#===========================================================================================
def display_information():
    global count    
    string_temp = "{:.1f}".format(dht_sensor.get_average_temperature())
    string_humi = "{:.1f}".format(dht_sensor.get_average_humidity())
    string_dust = "{:.6f}".format(dust_sensor.get_ugm3());
    string_snd  = "{:4d}".format(sound_sensor.get_max_sound());
    
    oled.clear()
    oled.setLine(1, 'sch_iot_0.96')                             # OLED 모듈 1번 줄에 저장
    oled.setLine(2, 'temp: ' + string_temp + 'C')               # OLED 모듈 2번 줄에 저장
    oled.setLine(3, 'humi: ' + string_humi + '%')               # OLED 모듈 3번 줄에 저장
    oled.setLine(4, 'dust: ' + string_dust )                    # OLED 모듈 4번 줄에 저장
    oled.setLine(5, 'snd : ' + string_snd)                      # OLED 모듈 5번 줄에 저장
    oled.setLine(6, 'cnt : ' + str(count))  
    oled.display()                                              # 저장된 내용을 oled에 보여줌    
    

#===========================================================================================
# 메시지 송신
#===========================================================================================
def send_message():
    app.add_sensor_data("temperature", dht_sensor.get_average_temperature());
    app.add_sensor_data("humidity", dht_sensor.get_average_humidity());
    app.add_sensor_data("dust", dust_sensor.get_ugm3());
    app.add_sensor_data("max_sound", sound_sensor.get_max_sound());
    app.send_sensor_data();
    print("send_message")


#===========================================================================================
# 메시지 수신
#===========================================================================================
def recv_message(cmnd, msg):
    pass


#===========================================================================================
# 시작 지점                     
#===========================================================================================
if __name__ == "__main__":
    setup(app, et_setup)    
    while True:
        loop(app, et_loop, et_short_periodic_process, et_long_periodic_process)


#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================
