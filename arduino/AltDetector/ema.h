#ifndef _EMA_H
#define _EMA_H

#include <stdint.h>

// March 2016, David Jacobowitz, david.jacobowitz@gmail.com

// This class implements a simple EMA filter. That is
//
// y[n] = a * x[n] + (1-a) * y[n-1]
//
// Because we seek to be fixed-point friendly, we 
// define:
//
// a = ALPHA / DENOM
//
// Where both ALPHA < DENOM so that 0 < a < 1.
//
// However, to get the compiler to emit efficient code,
// and particularly, code light on multiplies, choose
// ALPHA and DENOM that are powers of two, such as 1 and 256.
//
// Also, to get the compiler to use shifts instead of multiplies,
// it must see the filter constants as literals rather than 
// variables. That's why this is a template. 
//
// The state variable of this filter is essentially always
// left-shifted by DENOM,  so the larger the DENOM you choose,
// say, for more filtering, will also use up some upper bits
// of the state variable, so your range will be reduced.
//
// One solution to this is to use a larger type for the
// state variable. Of course, you could also use fp types, 
// too. The types are parameterized in this tempate for that 
// purpose.  

template <typename SAMP_TYPE, typename STORE_TYPE, 
	  uint32_t ALPHA, uint32_t DENOM>
class ema_c {
 public:
  ema_c() { };

  // primes the filter with a starting value
  void init(SAMP_TYPE sample) {
    curr_avg = sample * DENOM;
  }

  // call every time you have a new sample, returns the
  // current filter out, eg, "trailing average"
  inline SAMP_TYPE update(SAMP_TYPE sample) {
    curr_avg = ((ALPHA * sample) +
	        curr_avg - 
		((ALPHA * curr_avg) / DENOM)
	       );
    return get();
  }

  // turn the current sample average without updating
  inline SAMP_TYPE get() { return (curr_avg / DENOM); }
  
  // implements a biased updated that generates a kind of
  // trailing maximum. If an input value is higher than the 
  // current filter value, that becomes the new filter value,
  // if it is lower, then it goes into the filter normally.
  // This can be used to implement a "local" max function
  // without needing to maintain a long array of trailing 
  // values
  inline SAMP_TYPE upmax(SAMP_TYPE sample) {
    if (sample > get()) {
      init(sample);
    } else {
      update(sample);
    }
    return get();
  }
  
  
  // same as above, but for minimums
  inline SAMP_TYPE upmin(SAMP_TYPE sample) {
    if (sample < get()) {
      init(sample);
    } else {
      update(sample);
    }
    return get();
  }
  
 private:
  volatile STORE_TYPE curr_avg;
};

#endif


