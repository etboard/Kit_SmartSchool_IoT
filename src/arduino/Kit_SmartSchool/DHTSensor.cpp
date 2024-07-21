/******************************************************************************************
 * FileName     : DHTSensor.cpp 
 * Description  : DHT 센서
 * Author       : SCS
 * Created Date : 2024.07.21
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/

#include "DHTSensor.h"

DHTSensor::DHTSensor(uint8_t pin, uint8_t type) : _dht(pin, type), _readIndex(0), _firstCycle(true) {
    for (int i = 0; i < READINGS_COUNT; i++) {
        _temperatureReadings[i] = 0;
        _humidityReadings[i] = 0;
    }
}

void DHTSensor::begin() {
    _dht.begin();
}

void DHTSensor::update() {
    float humidity = _dht.readHumidity();
    float temperature = _dht.readTemperature();

    if (!isnan(humidity) && !isnan(temperature)) {
        _humidityReadings[_readIndex] = humidity;
        _temperatureReadings[_readIndex] = temperature;
        
        _readIndex = (_readIndex + 1) % READINGS_COUNT;
        if (_readIndex == 0) _firstCycle = false;
    }
}

float DHTSensor::getTemperature() {
    return calculateAverage(_temperatureReadings);
}

float DHTSensor::getHumidity() {
    return calculateAverage(_humidityReadings);
}

float DHTSensor::calculateAverage(float* readings) {
    float sum = 0;
    int count = _firstCycle ? _readIndex : READINGS_COUNT;
    
    for (int i = 0; i < count; i++) {
        sum += readings[i];
    }
    
    return count > 0 ? sum / count : 0;
}

//==========================================================================================
// End of Line
//==========================================================================================
