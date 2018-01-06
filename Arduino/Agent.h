#ifndef Agent_h
#define Agent_h

#include "Arduino.h"
#include "Motor.h"

class Agent
{
  public:
    Agent(HardwareSerial *serial);
    void SendMessage(String content);
    void ReceiveMessage(String content);
    void Act();
    void Stop();

  protected:    
    HardwareSerial * _serial;
    Motor * _base;
    Motor * _shaft1;
    Motor * _shaft2;
    Motor * _shaft3;
    Motor * _shaft4;
    Motor * _tool;

    void Agent::ProcessCommand(String command, int value);
};

#endif