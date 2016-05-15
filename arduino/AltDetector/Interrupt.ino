
const uint8_t SIG_TRAIL_LENGTH = 6;
uint16_t sig_trailing[SIG_TRAIL_LENGTH];

uint32_t last_peak_time = 0;




void interruptSetup(){     
  // Initializes Timer2 to throw an interrupt every 2mS.
  Signal = analogRead(pulsePin);
  smooth1.init(Signal);
  maxfilt.init(Signal);
  minfilt.init(Signal);
  last_peak_time = millis();
  
  TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE
  TCCR2B = 0x06;     // DON'T FORCE COMPARE, 256 PRESCALER 
  OCR2A = 0X7C;      // SET THE TOP OF THE COUNT TO 124 FOR 500Hz SAMPLE RATE
  TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
  sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED      
} 


bool started_trough = false;
bool started_peak = true;

uint32_t trough_time;
uint32_t peak_time;


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

  uint16_t span = currMax - currMin;
  uint16_t top_thresh = currMax - (span / 4);
  uint16_t bottom_thresh = currMin + (span / 4);
  
  bool in_trough = SmoothSignal <= bottom_thresh;
  bool in_peak   = SmoothSignal >= top_thresh;
  
  if (in_trough && !started_trough && started_peak) {
    started_trough = true;
    started_peak = false;
    trough_time = now;
    // Serial.println("trough start");    
  } else if (in_peak && !started_peak && started_trough) {
    // Serial.println("peak start");
    started_peak = true;
    started_trough = false;
    uint32_t beat_length = now - last_peak_time;
    last_peak_time = now;

    for (uint8_t i=IBI_TRAIL_LENGTH-1;i>0;i--) ibi_trailing[i] = ibi_trailing[i-1];
    ibi_trailing[0] = beat_length;
    QS = true;
    
  }

  for (uint8_t i=SIG_TRAIL_LENGTH-1;i>0;i--) sig_trailing[i] = sig_trailing[i-1];
  sig_trailing[0] = SmoothSignal;
  
  sei();                                     // enable interrupts when youre done!
}// end isr




