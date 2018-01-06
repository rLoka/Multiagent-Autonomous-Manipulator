#include "Arduino.h"
#include "Servo.h"
#include "Motor.h"

Motor::Motor(int pin, int startingPosition, int lowerBound = 0, int upperBound = 180)
{
    _servo.attach(pin);
    _startingPosition = startingPosition;
    _lowerBound = lowerBound;
    _upperBound = upperBound;

    Reset();
}

void Motor::Reset()
{
    MoveToPosition(_startingPosition);
}

void Motor::MoveToPosition(int position, int delayTime = 1)
{
    int currentPosition = GetPosition();

    if(position > currentPosition)
    {
        for(; currentPosition < position; currentPosition++)
        {
            SetPosition(currentPosition);
            delay(delayTime);
        }
    }
    else
    {
        for(; currentPosition > position; currentPosition--)
        {
            SetPosition(currentPosition);
            delay(delayTime);
        }
    } 
}

void Motor::Move(int step = 1)
{
    SetPosition(GetPosition() + step);
}

void Motor::MoveUp(int step = 1)
{
    SetPosition(GetPosition() + step);
}

void Motor::MoveDown(int step = 1)
{
    SetPosition(GetPosition() - step);
}

bool Motor::SetPosition(int position)
{
    if(position <= _upperBound && position >= _lowerBound)
    {
        _servo.write(position);
        return true;
    }

    return false;
}

int Motor::GetPosition()
{
    return _servo.read();
}
