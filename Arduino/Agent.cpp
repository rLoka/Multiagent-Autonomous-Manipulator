#include "Arduino.h"
#include "Motor.h"
#include "Agent.h"


//public
Agent::Agent(HardwareSerial *serial)
{
    _serial = serial;

    _base = new Motor(8, 75, 0, 180, 0);
    _shaft1 = new Motor(7, 80, 0, 180, 50);
    _shaft2 = new Motor(5, 90, 0, 180, 15);
    _shaft3 = new Motor(4, 30, 0, 180, 0);
    _shaft4 = new Motor(3, 80, 0, 180, 0);
    _tool = new Motor(2, 111, 110, 180, 5);
}

void Agent::SendMessage(String content)
{
    _serial->println(content);
}

void Agent::ReceiveMessage(String content)
{
    SendMessage(content);
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


//private
void Agent::ProcessCommand(String command, int value)
{
    if(command == "b")
    {
        _base->SetNextPosition(value);
    }
    else if(command == "s1")
    {
        _shaft1->SetNextPosition(value);
    }
    else if(command == "s2")
    {
        _shaft2->SetNextPosition(value);
    }
    else if(command == "s3")
    {
        _shaft3->SetNextPosition(value);
    }
    else if(command == "s4")
    {
        _shaft4->SetNextPosition(value);
    }
    else if(command == "t")
    {
        _tool->SetNextPosition(value);
    }
    else if(command == "sb")
    {
        _base->Move(value);
        PrintMotorPositions();
    }
    else if(command == "ss1")
    {
        _shaft1->Move(value);
        PrintMotorPositions();
    }
    else if(command == "ss2")
    {
        _shaft2->Move(value);
        PrintMotorPositions();
    }
    else if(command == "ss3")
    {
        _shaft3->Move(value);
        PrintMotorPositions();
    }
    else if(command == "ss4")
    {
        _shaft4->Move(value);
        PrintMotorPositions();
    }
    else if(command == "st")
    {
        _tool->Move(value);
        PrintMotorPositions();
    }
    else if(command == "e")
    {
        ExecuteMovement();
    }
    else if(command == "r")
    {
        Reset();
    }

}

void Agent::ExecuteMovement()
{
    bool b, s1, s2, s3, s4;

    do
    {
        s4 = _shaft4->MoveToPosition();
        b = _base->MoveToPosition();
        s3 = _shaft3->MoveToPosition();      
    } while(b || s3 || s4);

    do
    {          
        s2 = _shaft2->MoveToPosition();
        s1 = _shaft1->MoveToPosition();        
    } while(s1 || s2);

    delay(1000);

    while(_tool->MoveToPosition()){ continue; }

    delay(500);

    PrintMotorPositions();
    
}

void Agent::Reset()
{

}

void Agent::PrintMotorPositions()
{
    String motor = "b;" + String(_base->GetPosition()) + ";";
    motor += "s1;" + String(_shaft1->GetPosition()) + ";";
    motor += "s2;" + String(_shaft2->GetPosition()) + ";";
    motor += "s3;" + String(_shaft3->GetPosition()) + ";";
    motor += "s4;" + String(_shaft4->GetPosition()) + ";";
    motor += "t;" + String(_tool->GetPosition()) + ";";
    SendMessage(motor);
}