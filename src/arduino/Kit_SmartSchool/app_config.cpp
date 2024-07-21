/******************************************************************************************
 * FileName     : app_config.cpp
 * Description  : 응용 프로그램 구성 
 * Author       : SCS
 * Created Date : 2022.08.08
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/

#include "app_config.h"

//================================================-=========================================
// Include Componet header
//==========================================================================================
#include "./lib/etboard_oled_u8g2.h"                // ETboard OLED
#include "./lib/etboard_com.h"                      // ETboard common function
#include "./lib/etboard_wifi.h"                     // ETboard WiFi manager
#include "./lib/etboard_simple_mqtt.h"              // ETboard simple MQTT

#ifndef PLATFORMIO
  #include "./lib/etboard_oled_u8g2.cpp"
  #include "./lib/etboard_com.cpp"
  #include "./lib/etboard_wifi.cpp"  
  #include "./lib/etboard_simple_mqtt.cpp"
#endif

//==========================================================================================
// 전역 변수 선언                                   
//==========================================================================================
const char* board_hardware_verion = "ETBoard_V1.1";

//==========================================================================================
void setup()                                      // 설정 함수 
//==========================================================================================
{
  app.setup();                                    // 응용 프로그램 기본 설정

  custom_setup();                                 // 사용자 맞춤형 설정
}

//==========================================================================================
void loop()                                       // 반복 루틴
//==========================================================================================
{
  //----------------------------------------------------------------------------------------
  // MQTT 백그라운드 동작 
  //----------------------------------------------------------------------------------------
  app.mqtt.loop();

  //----------------------------------------------------------------------------------------
  // 사용자 맞춤형 반복 루틴
  //----------------------------------------------------------------------------------------
  custom_loop();                    

  //----------------------------------------------------------------------------------------
  // 사용자 맞춤형 반복 루틴                                // 1초
  //----------------------------------------------------------------------------------------
  if (millis() - app.lastShortMillis > SHORT_INTERVAL) {  
    custom_short_periodic_process();
    app.lastShortMillis = millis();                       // 현재 시각 업데이트
  }   

  //----------------------------------------------------------------------------------------
  // 사용자 맞춤형 반복 루틴                                // 5초
  //----------------------------------------------------------------------------------------
  if (millis() - app.lastLongMillis > LONG_INTERVAL) {  
    custom_long_periodic_process();
    app.lastLongMillis = millis();                        // 현재 시각 업데이트
  } 

  //----------------------------------------------------------------------------------------
  // 동작 상태 LED 깜밖이기
  //----------------------------------------------------------------------------------------  
  app.etboard.normal_blink_led();                 
}


//==========================================================================================
void onConnectionEstablished()                    // MQTT 연결되었을 때 동작하는 함수
//==========================================================================================
{
  app.mqtt.onConnectionEstablished();             // MQTT 연결되었을 때 동작  
}


//==========================================================================================
APP_CONFIG::APP_CONFIG() 
//==========================================================================================
{
  lastLongMillis = 0;                             // 최근 시각 초기화     
  lastShortMillis = 0;                            // 최근 시각 초기화     
  initailize_digital_value();                     // 디지털 값 초기화
}


//==========================================================================================
void APP_CONFIG::setup(void) 
//==========================================================================================
{

  //----------------------------------------------------------------------------------------
  // etboard 설정
  //----------------------------------------------------------------------------------------  
  etboard.setup();                                // ETboard 설정
  etboard.fast_blink_led();                       // 빠르게 eboard 작동 LED 깜밖임
  
  // 시리얼 모니터로 하드웨어 및 펌웨어 정보 출력
  etboard.print_board_information(board_hardware_verion, board_firmware_verion); 


  //----------------------------------------------------------------------------------------
  // oled
  //----------------------------------------------------------------------------------------
  oled.setup();                                   // OLED 설정
  display_BI();                                   // ketri 정보를 OLED에 표시

  //----------------------------------------------------------------------------------------
  // wifi
  //----------------------------------------------------------------------------------------  
  wifi.setup();                                   // WiFi 설정
  delay(500);                                     // 0.5초 대기

  //----------------------------------------------------------------------------------------
  // mqtt
  //----------------------------------------------------------------------------------------  
  mqtt.setup(
   wifi.mqtt_server,       // MQTT Broker server ip
   atoi(wifi.mqtt_port),   // The MQTT port, default to 1883. this line can be omitted);
   wifi.mqtt_user,         // Can be omitted if not needed  // Username
   wifi.mqtt_pass,         // Can be omitted if not needed  // Password
   "");                    // Client name that uniquely identify your device

  //----------------------------------------------------------------------------------------
  // initialize variables
  //----------------------------------------------------------------------------------------    
  lastLongMillis = millis();                          // 최근 시각 업데이트
}


//==========================================================================================
void APP_CONFIG::fast_blink_led(void) 
//==========================================================================================
{
  for(int i=0; i<10; i++) {
    digitalWrite(LED_BUILTIN, HIGH);              // 동작 LED 켜기
    delay(50);                                    // 0.05초 대기
    digitalWrite(LED_BUILTIN, LOW);               // 동작 LED 끄기
    delay(50);                                    // 0.05초 대기
  }
}


//==========================================================================================
void APP_CONFIG::display_BI(void) 
//==========================================================================================
{
  oled.setLine(1,"<ketri.re.kr>");                // 1번째 줄
  oled.setLine(2,"Welcome to");                   // 2번째 줄
  oled.setLine(3," ET-Board");                    // 3번재 줄
  oled.display();                                 // OLED에 표시
}

//==========================================================================================
void APP_CONFIG::dg_Write(int pin, int value)
//==========================================================================================
{
  mqtt.dg_Write(pin, value);
}

//==========================================================================================
void APP_CONFIG::update_digital_value(void)
//==========================================================================================
{ 
  mqtt.update_digital_value();
}

//==========================================================================================
bool APP_CONFIG::isChanged_digital_value(void)
//==========================================================================================
{ 
  return mqtt.isChanged_digital_value();
}

//==========================================================================================
void APP_CONFIG::initailize_digital_value()
//==========================================================================================
{
  mqtt.initailize_digital_value();
}

//==========================================================================================
int APP_CONFIG::dg_Read(int pin)
//==========================================================================================
{ 
  return mqtt.dg_Read(pin);
}

//==========================================================================================
// End of Line
//==========================================================================================
