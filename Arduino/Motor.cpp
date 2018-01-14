#include "Arduino.h"
#include "Servo.h"
#include "Motor.h"

Motor::Motor(int pin, int startingPosition, int lowerBound = 0, int upperBound = 180, int delayAdded = 50)
{
    _servo.attach(pin);
    _startingPosition = startingPosition;
    _nextPosition = startingPosition;
    _lowerBound = lowerBound;
    _upperBound = upperBound;
    _delay = delayAdded;
    Reset();
}

void Motor::Reset()
{
    SetPosition(_startingPosition);
}

void Motor::SetNextPosition(int position)
{
    _nextPosition = position;
}

bool Motor::MoveToPosition()
{
    int currentPosition = GetPosition();

    if(_nextPosition > currentPosition)
    {
        int difference = _nextPosition - currentPosition;
        SetPosition(currentPosition + 1);        
        delay(difference/3 + _delay);

        return true;
    }
    else if(_nextPosition < currentPosition)
    {
        int difference = currentPosition - _nextPosition;
        SetPosition(currentPosition - 1);
        delay(difference/3 + _delay);

        return true;
    }
    else
    {
        return false;
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
