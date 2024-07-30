/******************************************************************************************
 * FileName     : Kit_SmartSchool_IoT.ino
 * Description  : 이티보드로 온도/습소/미세먼지/소음을 측정하여 WiFi로 송신
 * Author       : SCS
 * Created Date : 2024.07.11
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/
const char* board_firmware_verion = "sch_iot_0.95";

//================================================-=========================================
// 응용 프로그램 구성 사용하기                       
//==========================================================================================
#include "app_config.h"
APP_CONFIG app;

//==========================================================================================
// 온습도 센서 사용하기
//==========================================================================================
#include "DHTSensor.h"                            // DHT 온습도 센서 사용
DHTSensor dhtSensor(D9);                          // D9 핀에 DHT11 센서 

//==========================================================================================
// 미세먼지 센서 사용하기
//==========================================================================================
#include "PPD42NS.h"                              // PPD42NS 미세 먼지 센서 
PPD42NS dustSensor(A4);                           // A4 핀에 센서 연결

//==========================================================================================
// 사운드 센서 사용하기
//==========================================================================================
#include "MAX9814.h"                              // MAX9814 사운드 센서 사용
MAX9814 soundSensor(A3);                          // A3번에 센서 연결


//==========================================================================================
// 상수 정의                                       
//==========================================================================================


//==========================================================================================
// 전역 변수 선언                                   
//==========================================================================================


//==========================================================================================
void custom_setup()                               // 사용자 맞춤형 설정 함수
//==========================================================================================
{
  dhtSensor.begin();                          
  dustSensor.begin();                         
  soundSensor.begin();                        
}


//==========================================================================================
void custom_loop()                                // 사용자 반복 처리
//==========================================================================================
{
  do_sensing_process();                           // 센싱 처리
}


//==========================================================================================
void do_sensing_process()                         // 센싱 처리 함수
//==========================================================================================
{ 
  dhtSensor.update();                             // 온습도 센서 업데이트
  soundSensor.update();                           // 사운드 센서 업데이트
  dustSensor.update();                            // 미세 먼지 센서 업데이트
}


//==========================================================================================
void custom_short_periodic_process()              // 사용자 주기적 처리 (예 : 1초마다)
//==========================================================================================
{   
  display_information();                          // 표시 처리
}


//==========================================================================================
void custom_long_periodic_process()               // 사용자 주기적 처리 (예 : 5초마다)
//==========================================================================================
{ 
  send_message();                                 // 메시지 송신
  soundSensor.reset();                            // 사운드 센서 리셋
}


//==========================================================================================
void display_information()                        // 센싱 정보 OLED 표시 함수
//==========================================================================================
{
  String string_temp = String(dhtSensor.getTemperature(), 1);  // 온도를 문자열로 변환
  String string_humi = String(dhtSensor.getHumidity(), 1);     // 습도를 문자열로 변환  
  String string_dust = String(dustSensor.getUgm3(), 2);        // 미세먼지를 문자열로 변환
  String string_sound = String(soundSensor.getMaxSound());     // 사운드를 문자열로 변환
  
  app.oled.setLine(1, board_firmware_verion);            // 1번째 줄에 펌웨어 버전  
  app.oled.setLine(2, string_temp + "/" + string_humi);  // 2번재 줄에 온도,  습도
  app.oled.setLine(3, string_dust + "/" + string_sound); // 3번재 줄에 미세먼지, 사운드
  app.oled.display();                                    // OLED에 표시
}


//==========================================================================================
void send_message()
//==========================================================================================
{
  (*app.mqtt.doc)["temperature"] = app.etboard.round2(dhtSensor.getTemperature());
  (*app.mqtt.doc)["humidity"]    = app.etboard.round2(dhtSensor.getHumidity());
  (*app.mqtt.doc)["max_sound"]   = soundSensor.getMaxSound();
  (*app.mqtt.doc)["dust"]        = dustSensor.getUgm3();

  app.mqtt.publish_tele("/sensor", (*app.mqtt.doc));     // 메시지 송신
}


//==========================================================================================
//                                                    
// (주)한국공학기술연구원 http://et.ketri.re.kr       
//                                                    
//==========================================================================================
