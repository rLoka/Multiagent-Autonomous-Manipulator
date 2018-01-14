import time
import serial
from Agent import Agent, AgentType
from Entities import Manipulator

class ControllingAgent(Agent):

    def __init__(self, agentType):
        Agent.__init__(self, agentType)
        self.Serial = serial.Serial("COM3", 9600)

    def AddPeerAgent(self, peerAgent):
        if peerAgent.AgentType == AgentType.KinematicsAgent:
            self._kinematicsAgent = peerAgent

    def SendMessage(self, receivingAgents, content):
        Agent.SendMessage(self, receivingAgents, content) 

    def ReceiveMessage(self, senderAgent, content):
        self.ExecuteGrab(content)
        self.LiftUp()
        self.ExecuteDrop()
        self.MoveToStartingPosition()
        self.SendMessage([self._kinematicsAgent], "Done")

    def Act(self):
        print "Act!"

    #internal methods
    def ExecuteGrab(self, manipulatorConfig):
        command = manipulatorConfig.ToText()
        command = command + "e;0;"
        self.Serial.write(command)
        print self.Serial.readline()    
        time.sleep(4)

    def MoveToStartingPosition(self):
        time.sleep(2)   
        self.Serial.write("s1;80;s2;90;e;0;")
        print self.Serial.readline()
        time.sleep(2)
        self.Serial.write("b;75;s3;30;s4;80;e;0;")
        print self.Serial.readline()
        time.sleep(5)  

    def ExecuteDrop(self):
        time.sleep(3)
        self.Serial.write("b;180;s1;122;s2;90;s3;32;s4;80;t;111;e;0;")
        print self.Serial.readline()    
        time.sleep(6)

    def LiftUp(self):
        time.sleep(2)   
        self.Serial.write("s1;80;s2;90;e;0;")
        print self.Serial.readline()
        time.sleep(2)
