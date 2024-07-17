#include "PPD42NS.h"

PPD42NS::PPD42NS(int sensorPin, unsigned long sampleTime) : 
  pin(sensorPin), 
  sampletime_ms(sampleTime),
  duration(0),
  starttime(0),
  lowpulseoccupancy(0),
  ugm3(0) {}

void PPD42NS::begin() {
  pinMode(pin, INPUT);
  starttime = millis();
}

void PPD42NS::update() {
  duration = pulseIn(pin, LOW);
  lowpulseoccupancy += duration;

  if ((millis() - starttime) > sampletime_ms) {
    calculate();
    printResults();
    reset();
  }
}

float PPD42NS::getUgm3() const { 
  return ugm3; 
}

void PPD42NS::calculate() {
  float ratio = lowpulseoccupancy / (sampletime_ms * 10.0);
  float concentration = 1.1 * pow(ratio, 3) - 3.8 * pow(ratio, 2) + 520 * ratio + 0.62;
  ugm3 = concentration * 100 / 13000;
}

void PPD42NS::printResults() {
  Serial.print("ugm3 = ");
  Serial.print(ugm3);
  Serial.println(" ug/m3");
}

void PPD42NS::reset() {
  lowpulseoccupancy = 0;
  starttime = millis();
}