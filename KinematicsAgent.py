import time
import serial
from Agent import Agent, AgentType

class KinematicsAgent(Agent):

    def __init__(self, agentType):
        Agent.__init__(self, agentType)

    def AddPeerAgent(self, peerAgent):
        Agent.__init__(self, peerAgent)

    def OnPeerAgentAdded(self):
        raise NotImplementedError

    def SendMessage(self, receivingAgents, content):
        Agent.SendMessage(self, receivingAgents, content) 

    def ReceiveMessage(self, senderAgent, content):
        print "Primljeno: " + content

    def Act(self):
        raise NotImplementedError

k = KinematicsAgent(AgentType.KinematicsAgent)
k.SendMessage([k], "LOL!")
ser = serial.Serial("COM3", 9600)