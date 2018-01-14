import time
import serial
from Agent import Agent, AgentType

class SupervisorAgent(Agent):

    def __init__(self, agentType):
        Agent.__init__(self, agentType)

    def AddPeerAgent(self, peerAgent):
        if peerAgent.AgentType == AgentType.LearningAgent:
            self._learningAgent = peerAgent

    def SendMessage(self, receivingAgents, content):
        Agent.SendMessage(self, receivingAgents, content) 

    def ReceiveMessage(self, senderAgent, content):
        raise NotImplementedError

    def Act(self):
        print "Act!"

    #internal methods