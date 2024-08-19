/******************************************************************************************
 * FileName     : 1_ Sound_max9814.ino
 * Description  : 사운드 센서 max9814를 사용하여 소음 수준을 모니터링
 * Author       : SCS
 * Created Date : 2024.07.13
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/

const int sound_pin = A3;                         // 사운드센서 MAX9814 pin 지정
int sound_result = 0;                             // 사운드센서 측정 값
int max_sound = 0;                                // 사운드센서 최대 값
int sound_count = 0;                              // 사운드센서 카운트

void setup() 
{
  Serial.begin(115200);
}

void loop() 
{
  get_sound();
  
  delay(2);  
}

//==========================================================================================
void get_sound()                                  // 사운드 센싱
//==========================================================================================
{ 
  // read the analog in value:
  sound_result = analogRead(sound_pin);
  if (sound_result > max_sound) {
    max_sound = sound_result;
  }  
  sound_count++;
  if (sound_count > 100) {
    max_sound = 0;
    sound_count=0;
  }
  // print the results to the Serial Monitor:
  Serial.print("0\t");
  Serial.print("1000\t");
  Serial.print("2500\t");
  Serial.print("4000\t");
  Serial.print(sound_result);Serial.print("\t");  
  Serial.print(max_sound);                   
  Serial.println();                   
}

//==========================================================================================
//                                                    
// (주)한국공학기술연구원 http://et.ketri.re.kr       
//                                                    
//==========================================================================================
