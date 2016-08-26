#include <Arduino.h>

void setup() {
  // Initialize the serial port to send data back to the PC
  Serial.begin(115200);

  // set pin A0 as an input, so it can be read
  pinMode(A0, INPUT);
};

void loop() {
  // read the voltage on the input pin
  int sensor_value = analogRead(A0);

  // print out the value
  Serial.println(sensor_value);

  // wait 100 milliseconds
  delay(100);
}

