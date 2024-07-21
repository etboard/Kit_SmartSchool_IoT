/******************************************************************************************
 * FileName     : MAX9814.cpp 
 * Description  : MAX9814 사운드 센서
 * Author       : SCS
 * Created Date : 2024.07.21
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/

#include "MAX9814.h"

MAX9814::MAX9814(int pin) : _pin(pin), _maxSound(0) {}

void MAX9814::begin() {
    pinMode(_pin, INPUT);
}

void MAX9814::update() {
    int soundResult = analogRead(_pin);
    if (soundResult > _maxSound) {
        _maxSound = soundResult;
    }
}

void MAX9814::reset() {
    _maxSound = 0;
}

int MAX9814::getMaxSound() const {
    return _maxSound;
}

//==========================================================================================
// End of Line
//==========================================================================================
