#ifndef Motor_h
#define Motor_h

#include "Arduino.h"
#include "Servo.h"

class Motor
{
  public:
    Motor(int pin, int startingPosition, int lowerBound = 0, int upperBound = 180, int delayAdded = 50);
    void Reset();
    void SetNextPosition(int position);
    bool MoveToPosition();
    void Move(int step = 1);
    void MoveUp(int step = 1);
    void MoveDown(int step = 1);
    int GetPosition();
    bool SetPosition(int position); 

  private:       
    Servo _servo;
    int _startingPosition;
    int _lowerBound;
    int _upperBound;
    int _nextPosition;
    int _delay;
};

#endif