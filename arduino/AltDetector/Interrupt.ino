
uint32_t last_peak_time = 0;
bool started_trough = false;
bool started_peak = true;
uint32_t trough_time;


void interruptSetup(){     
  // Initializes Timer2 to throw an interrupt every 2mS.
  Signal = analogRead(pulsePin);
  smooth1.init(Signal);
  maxfilt.init(Signal);
  minfilt.init(Signal);
  last_peak_time = millis();
  first_ibi = true;
  
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
  uint32_t now = millis();
  Signal = analogRead(pulsePin);

  uint16_t SmoothSignal = smooth1.update(Signal);
  uint16_t currMax = maxfilt.upmax(SmoothSignal);
  uint16_t currMin = minfilt.upmin(SmoothSignal);

  uint16_t span = currMax - currMin;
  uint16_t top_thresh = currMax - (span / 4);
  uint16_t bottom_thresh = currMin + (span / 4);
  
  bool in_trough = SmoothSignal <= bottom_thresh;
  bool in_peak   = SmoothSignal >= top_thresh;
  
  if (in_trough && !started_trough) {
    started_trough = true;
    trough_time = now;

  } else if (in_peak && started_trough) {
    started_trough = false;
    uint32_t beat_length = now - last_peak_time;
    last_peak_time = now;

    if (first_ibi) {
      ibiflt.init(beat_length);
      first_ibi = false;
    } else {
      ibiflt.update(beat_length);
    }
    pulse_ready = true;
  }

  sei();                                     // enable interrupts when youre done!
}// end isr




