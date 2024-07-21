/******************************************************************************************
 * FileName     : MAX9814.h
 * Description  : MAX9814 사운드 센서
 * Author       : SCS
 * Created Date : 2024.07.21
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/

#ifndef SOUND_SENSOR_H
#define SOUND_SENSOR_H

#include <Arduino.h>

class MAX9814 {
public:
    MAX9814(int pin);
    void begin();
    void update();
    void reset();
    int getMaxSound() const;

private:
    int _pin;
    int _maxSound;
};

#endif // SOUND_SENSOR_H

//==========================================================================================
// End of Line
//==========================================================================================
