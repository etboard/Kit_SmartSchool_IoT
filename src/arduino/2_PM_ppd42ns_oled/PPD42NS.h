#ifndef PPD42NS_H
#define PPD42NS_H

#include <Arduino.h>

class PPD42NS {
private:
  int pin;
  unsigned long duration;
  unsigned long starttime;
  unsigned long sampletime_ms;
  unsigned long lowpulseoccupancy;
  float ugm3;

  void calculate();
  void printResults();
  void reset();

public:
  PPD42NS(int sensorPin, unsigned long sampleTime = 30000);
  void begin();
  void update();
  float getUgm3() const;
};

#endif