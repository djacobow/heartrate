/*

15 May 2016
David G. Jacobowitz
david.jacobowitz@gmail.com


Inspired by the PulseSensor Amped code by Joel Murphy and Yuri Gitman, 
this is an alternative approach to the same problem of interpreting
heartbeats from a stream of heartbeat data.

The heuristic employed here is totally different. The data is collected
at the same rate from the interrupt. From there, it is smoothed (low-
pass filtered) by a simple one-pole IIR filter to reduce noise. Two 
other similar filters help maintain recent maxima and minima for the 
wavefrom. More intuitively, one might use a sliding window filter in 
order to maintain a "trailing average", but for the length of averaging
I want, that memory cost of the required arrays would be prohibitive on 
the Arduino. The nice thing about the IIR filters is that they only 
require one state variable and are also cheap to compute if you use a 
denominator that is a power of two (so the division can be done as a 
shift).

*/


#include "shared.h"

//  VARIABLES
int pulsePin = 0;                 // Pulse Sensor purple wire connected to analog pin 0
int blinkPin = 13;                // pin to blink led at each beat
int fadePin = 5;                  // pin to do fancy classy fading blink at each beat
int fadeRate = 0;                 // used to fade LED on with PWM on fadePin

void setup(){
  pinMode(blinkPin,OUTPUT);         // pin that will blink to your heartbeat!
  pinMode(fadePin,OUTPUT);          // pin that will fade to your heartbeat!
  pinMode(pulsePin,INPUT);
  
  Serial.begin(115200);
  interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS 
   // UN-COMMENT THE NEXT LINE IF YOU ARE POWERING The Pulse Sensor AT LOW VOLTAGE, 
   // AND APPLY THAT VOLTAGE TO THE A-REF PIN
   //analogReference(EXTERNAL);   
}



void loop(){
  // send Processing the slightly cooked Pulse Sensor data
  sendDataToProcessing('S', smooth1.get());

  if (pulse_ready){
        fadeRate = 255;                  // Set 'fadeRate' Variable to 255 to fade LED with pulse
        digitalWrite(blinkPin,1);
        uint16_t bpm = 0;
        uint16_t ibi = 0;
        if (calcbpm(bpm,ibi)) {
          sendDataToProcessing('B',bpm);
          sendDataToProcessing('Q',ibi);
        }
        pulse_ready = false;
     }
  delay(20);                             //  take a break
  ledFadeToBeat();
}


void ledFadeToBeat(){
    fadeRate -= 15;                         //  set LED fade value
    fadeRate = constrain(fadeRate,0,255);   //  keep LED fade value from going into negative numbers!
    analogWrite(fadePin,fadeRate);          //  fade LED
    digitalWrite(blinkPin,0);
  }


void sendDataToProcessing(char symbol, int data ){
    Serial.print(symbol);                // symbol prefix tells Processing what type of data is coming
    Serial.println(data);                // the data to send culminating in a carriage return
  }







