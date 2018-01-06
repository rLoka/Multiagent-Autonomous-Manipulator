#include "Arduino.h"
#include "Motor.h"
#include "Agent.h"


//public
Agent::Agent(HardwareSerial *serial)
{
    _serial = serial;

    _base = new Motor(8, 75, 0, 180);
    _shaft1 = new Motor(7, 80, 0, 180);
    _shaft2 = new Motor(5, 90, 0, 180);
    _shaft3 = new Motor(4, 30, 0, 180);
    _shaft4 = new Motor(3, 80, 0, 180);
    _tool = new Motor(2, 110, 0, 120);
}

void Agent::SendMessage(String content)
{
    _serial->println(content);
}

void Agent::ReceiveMessage(String content)
{
    int delimiterIndex = 0;

    String command = "";
    int value = 1;

    for (int i = 0; i < content.length(); i++)
    {
        if (content[i] == ';')
        {
            if(command == "")
            {
                command = content.substring(delimiterIndex, i);
            }
            else
            {
                value = content.substring(delimiterIndex, i).toInt();                
                ProcessCommand(command, value);
                command = "";
            }
            delimiterIndex = i + 1;
        }
    }
}


void Agent::Act()
{
}

void Agent::Stop()
{
}

//private
void Agent::ProcessCommand(String command, int value)
{
    //delay?
    if(command == "b")
    {
        _base->Move(value);
    }
    else if(command == "s1")
    {
        _shaft1->Move(value);
    }
    else if(command == "s2")
    {
        _shaft2->Move(value);
    }
    else if(command == "s3")
    {
        _shaft3->Move(value);
    }
    else if(command == "s4")
    {
        _shaft4->Move(value);
    }
    else if(command == "t")
    {
        _tool->Move(value);
    }
    else if(command == "r")
    {
        _tool->Move(value);
    }

    _serial->println(command);
    _serial->println(value);
}
