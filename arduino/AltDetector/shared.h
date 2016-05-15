#ifndef _SHARED_H
#define _SHARED_H

#include "ema.h"
#include <stdint.h>

const uint8_t IBI_TRAIL_LENGTH = 4;
extern uint16_t ibi_trailing[IBI_TRAIL_LENGTH];
extern ema_c<uint16_t,uint16_t,1,32> smooth1;
extern ema_c<uint16_t,uint32_t,1,1024> maxfilt;
extern ema_c<uint16_t,uint32_t,1,1024> minfilt;
extern volatile uint16_t Signal;  
extern volatile bool QS;

#endif

