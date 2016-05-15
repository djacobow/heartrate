#include "shared.h"

uint16_t ibi_trailing[IBI_TRAIL_LENGTH];

ema_c<uint16_t,uint16_t,1,32> smooth1;
ema_c<uint16_t,uint32_t,1,1024> maxfilt;
ema_c<uint16_t,uint32_t,1,1024> minfilt;

volatile uint16_t Signal;
volatile uint16_t SmoothSignal;

volatile bool QS = false;

