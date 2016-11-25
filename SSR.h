#ifndef SSR_h
#define SSR_h

#define SSR_PINa 8
#define SSR_PINb 9
#define SSR_PINc 10

#define PUMP_PIN 11

inline void SSRInit()
{
  pinMode(SSR_PINa, OUTPUT);
  pinMode(SSR_PINb, OUTPUT);
  pinMode(SSR_PINc, OUTPUT);

  digitalWrite(SSR_PINa, LOW);
  digitalWrite(SSR_PINb, LOW);
  digitalWrite(SSR_PINc, LOW);
}

inline void SSROn()
{ 
  digitalWrite(SSR_PINa, HIGH);
  digitalWrite(SSR_PINb, HIGH);
  digitalWrite(SSR_PINc, HIGH);  
}

inline void SSROff()
{
  digitalWrite(SSR_PINa, LOW);
  digitalWrite(SSR_PINb, LOW);
  digitalWrite(SSR_PINc, LOW);
}

inline void SSRPhase(float diff)
{ 
  SSROff();
  if(diff > 4.5f)
  {
    digitalWrite(SSR_PINa, HIGH);
    digitalWrite(SSR_PINb, HIGH);
    digitalWrite(SSR_PINc, HIGH); 
  } else if (diff > 3.0f){
    digitalWrite(SSR_PINb, HIGH);
    digitalWrite(SSR_PINc, HIGH);
  } else if (diff > 1.5f){
    digitalWrite(SSR_PINa, HIGH);
    digitalWrite(SSR_PINb, HIGH);
  } else if (diff > 0.5f){
    digitalWrite(SSR_PINc, HIGH);
  } else {
    digitalWrite(SSR_PINb, HIGH);
  }
}
}

inline void PumpOn()
{
  digitalWrite(PUMP_PIN, HIGH);
}

inline void PumpOff()
{
  digitalWrite(PUMP_PIN, LOW);
}

#endif
