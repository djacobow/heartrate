#include <stdint.h>


uint32_t i;

void setup(){
  Serial.begin(115200);
  i = 0;
}



void loop(){
  
  float angle = (2.0 * 3.14159265358 / 80) * (float)(i % 80);
  float val = 300 * (1 + sin(angle));
  sendDataToProcessing('S', val);
  if ((i % 80) == 0) sendDataToProcessing('B',random(100));
  if ((i % 80) == 39) sendDataToProcessing('Q',random(100));
  i++;
  delay(20);                             //  take a break
}

void sendDataToProcessing(char symbol, int data ){
    Serial.print(symbol);                // symbol prefix tells Processing what type of data is coming
    Serial.println(data);                // the data to send culminating in a carriage return
  }







