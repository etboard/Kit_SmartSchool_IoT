/******************************************************************************************
 * FileName     : DHTSensor.h
 * Description  : DHT 센서
 * Author       : SCS
 * Created Date : 2024.07.21
 * Reference    : 
 * Modified     : 
 * Modified     : 
******************************************************************************************/
#ifndef DHT_SENSOR_H
#define DHT_SENSOR_H

#include <DHT.h>

class DHTSensor {
public:
    DHTSensor(uint8_t pin, uint8_t type = DHT11);
    void begin();
    void update();
    float getTemperature();
    float getHumidity();

private:
    DHT _dht;
    static const int READINGS_COUNT = 10;
    float _temperatureReadings[READINGS_COUNT];
    float _humidityReadings[READINGS_COUNT];
    int _readIndex;
    bool _firstCycle;

    float calculateAverage(float* readings);
};

#endif // DHT_SENSOR_H

//==========================================================================================
// End of Line
//==========================================================================================
