#include "Agent.h"
#include "Motor.h"

Agent *ControllingAgent;
String message;

void setup()
{
    Serial.begin(9600);
    ControllingAgent = new Agent(&Serial);
    ControllingAgent->Act();
}

void loop()
{
    while (Serial.available())
    {
        char chr = Serial.read();
        message += chr;
        delay(2);
    }

    if (message.length() > 0)
    {
        ControllingAgent->ReceiveMessage(message);
        message = "";
    }
}