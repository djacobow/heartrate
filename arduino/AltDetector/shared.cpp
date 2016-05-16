#include "shared.h"
#include <Arduino.h>

bool first_ibi;
ema_c<uint16_t,uint16_t,1,32> smooth1;
ema_c<uint16_t,uint32_t,1,1024> maxfilt;
ema_c<uint16_t,uint32_t,1,1024> minfilt;
ema_c<uint16_t,uint16_t,1,4> ibiflt;

volatile uint16_t Signal;
volatile uint16_t SmoothSignal;

volatile bool pulse_ready  = false;


// calculates the beats per minute from the 
// current trailing inter-beat-interval average.
// Also guards against sending ridiculous values
bool calcbpm(uint16_t &bpm, uint16_t &ibi) {
 if (!first_ibi) {
   uint16_t avg = ibiflt.get();
   // NB: the lowest recorded heart rate in a healthy human is 26bpm, 
   // out 2400 ms between beats. 
   if ((avg <= 2400) && (avg >= 200)) {
     ibi = avg;
     bpm = 60000UL / (uint32_t)avg;
     return true;
   }
 }
 return false;
};


