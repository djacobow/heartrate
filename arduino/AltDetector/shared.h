#ifndef _SHARED_H
#define _SHARED_H

#include "ema.h"
#include <stdint.h>

extern bool first_ibi;
extern ema_c<uint16_t,uint16_t,1,32> smooth1;
extern ema_c<uint16_t,uint32_t,1,1024> maxfilt;
extern ema_c<uint16_t,uint32_t,1,1024> minfilt;
extern ema_c<uint16_t,uint16_t,1,4> ibiflt;

extern volatile uint16_t Signal;  
extern volatile bool pulse_ready;
bool calcbpm(uint16_t &bpm, uint16_t &ibi);

#endif

