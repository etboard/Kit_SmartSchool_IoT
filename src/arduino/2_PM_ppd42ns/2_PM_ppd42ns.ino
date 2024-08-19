/******************************************************************************************
 * FileName     : 2_PM_ppd42ns.ino
 * Description  : 미세먼지 센서 PPD42NS를 사용하여 미세 먼지를 모니터링
 * Author       : SCS
 * Created Date : 2024.07.13
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/

#include "PPD42NS.h"

PPD42NS dustSensor(A4);  // 8번 핀에 연결된 센서로 PPD42NS 객체 생성

unsigned long lastPrintTime = 0;  // 마지막 출력 시간을 저장할 변수
const unsigned long printInterval = 1000 * 5;  // 출력 간격 (1000ms = 1초)

void setup() {
  Serial.begin(115200);
  Serial.println("start");
  dustSensor.begin();
}

void loop() {
  dustSensor.update();  // 센서 데이터 업데이트

  unsigned long currentTime = millis();
  
  // 1초가 지났는지 확인
  if (currentTime - lastPrintTime >= printInterval) {
    // getUgm3 값을 출력
    Serial.print("Current ugm3: ");
    Serial.print(dustSensor.getUgm3());
    Serial.println(" ug/m3");

    lastPrintTime = currentTime;  // 마지막 출력 시간 업데이트
  }
}


//==========================================================================================
//                                                    
// (주)한국공학기술연구원 http://et.ketri.re.kr       
//                                                    
//==========================================================================================
