/******************************************************************************************
 * FileName     : app_config.h
 * Description  : 응용 프로그램 구성 
 * Author       : SCS
 * Created Date : 2022.08.08
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/

#ifndef APP_CONFIG_H
#define APP_CONFIG_H

/*
#include "lib/etboard_com.h"
#include "lib/etboard_simple_mqtt.h"
#include "lib/etboard_oled_u8g2.h"
#include "lib/etboard_wifi.h"
*/

#include "./lib/etboard_com.h"
#include "./lib/etboard_simple_mqtt.h"
#include "./lib/etboard_oled_u8g2.h"
#include "./lib/etboard_wifi.h"

extern const char* board_firmware_verion;
extern void custom_setup();
extern void custom_loop();
extern void custom_long_periodic_process();
extern void custom_short_periodic_process();

extern class APP_CONFIG app;

//------------------------------------------------------------------------------------------
// 메시지 송신 주기 : 주의!!!! 너무 빨리 또는 많이 보내면 서버에서 거부할 수 있음(Banned)
//------------------------------------------------------------------------------------------
#define LONG_INTERVAL  (1000 * 5)                 // 권장 5초 (단위: 초/1000)

//------------------------------------------------------------------------------------------
// 메시지 표시 주기
//------------------------------------------------------------------------------------------
#define SHORT_INTERVAL  (1000 * 1)                // 권장 1초 (단위: 초/1000)


//==========================================================================================
class APP_CONFIG 
//==========================================================================================
{

  private:      
  
  public:          
    unsigned lastLongMillis;
    unsigned lastShortMillis;
    String operation_mode = "automatic";
    bool bDigitalChanged = false;
    
    ETBOARD_OLED_U8G2 oled;
    ETBOARD_COM etboard;
    ETBOARD_SIMPLE_MQTT mqtt; 
    ETBOARD_WIFI wifi;   
    
    APP_CONFIG();
    void setup(void);    
    void fast_blink_led(void);
    void normal_blink_led(void); 
    void display_BI(void);

    void dg_Write(int pin, int value);
    void update_digital_value();
    bool isChanged_digital_value(void);
    void initailize_digital_value(void);
    int  dg_Read(int pin);
    
};

#endif

//==========================================================================================
// End of Line
//==========================================================================================
