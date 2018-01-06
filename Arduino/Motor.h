#ifndef Motor_h
#define Motor_h

#include "Arduino.h"
#include "Servo.h"

class Motor
{
  public:
    Motor(int pin, int startingPosition, int lowerBound = 0, int upperBound = 180);
    void Reset();
    void MoveToPosition(int position, int delay = 1);
    void Move(int step = 1);
    void MoveUp(int step = 1);
    void MoveDown(int step = 1);
    int CurrentPosition();

  private:
    bool SetPosition(int position);
    int GetPosition();
    Servo _servo;
    int _startingPosition;
    int _lowerBound;
    int _upperBound;
};

#endif