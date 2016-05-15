
const uint8_t SIG_TRAIL_LENGTH = 6;
uint16_t sig_trailing[SIG_TRAIL_LENGTH];

uint32_t last_beat = 0;




void interruptSetup(){     
  // Initializes Timer2 to throw an interrupt every 2mS.
  Signal = analogRead(pulsePin);
  smooth1.init(Signal);
  maxfilt.init(Signal);
  minfilt.init(Signal);
  last_beat = millis();
  
  TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE
  TCCR2B = 0x06;     // DON'T FORCE COMPARE, 256 PRESCALER 
  OCR2A = 0X7C;      // SET THE TOP OF THE COUNT TO 124 FOR 500Hz SAMPLE RATE
  TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
  sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED      
} 


// THIS IS THE TIMER 2 INTERRUPT SERVICE ROUTINE. 
// Timer 2 makes sure that we take a reading every 2 miliseconds
ISR(TIMER2_COMPA_vect){                         // triggered when Timer2 counts to 124
  cli();                                      // disable interrupts while we do this
  Signal = analogRead(pulsePin);
  int SmoothSignal = smooth1.update(Signal);
  uint32_t now = millis();
  if (SmoothSignal > maxfilt.get()) {
    maxfilt.init(SmoothSignal);
  } else {
    maxfilt.update(SmoothSignal);
  }

  if (Signal < minfilt.get()) {
    minfilt.init(SmoothSignal);
  } else {
    minfilt.update(SmoothSignal);
  }
  
  int currMax = maxfilt.get();
  int currMin = minfilt.get();

  int span = currMax - currMin;
  int top_thresh = currMax - (span / 4);
  int bottom_thresh = currMin + (span / 4);
  // bool new_beat = ((SmoothSignal <= bottom_thresh) && (sig_trailing[5] >= top_thresh));
  bool new_beat = (SmoothSignal <= bottom_thresh);
  
  uint32_t beat_length = now - last_beat;
  new_beat &= (beat_length >= 240);
  
  if (new_beat) {
    for (uint8_t i=IBI_TRAIL_LENGTH-1;i>0;i--) ibi_trailing[i] = ibi_trailing[i-1];
    ibi_trailing[0] = beat_length;
    last_beat = now;
    QS = true;
  }

  for (uint8_t i=SIG_TRAIL_LENGTH-1;i>0;i--) sig_trailing[i] = sig_trailing[i-1];
  sig_trailing[0] = SmoothSignal;
  
  sei();                                     // enable interrupts when youre done!
}// end isr




