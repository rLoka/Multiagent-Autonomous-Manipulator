import time
import serial
from Agent import Agent, AgentType

class LearningAgent(Agent):
    def __init__(self, agentType):
        Agent.__init__(self, agentType)

    def AddPeerAgent(self, peerAgent):
        if peerAgent.AgentType == AgentType.SensorAgent:
            self._sensorAgent = peerAgent
        elif peerAgent.AgentType == AgentType.KinematicsAgent:
            self._kinematicsAgent = peerAgent
        elif peerAgent.AgentType == AgentType.SupervisorAgent:
            self._supervisorAgent = peerAgent

    def SendMessage(self, receivingAgents, content):
        Agent.SendMessage(self, receivingAgents, content) 

    def ReceiveMessage(self, senderAgent, content):
        if senderAgent.AgentType == AgentType.SensorAgent:
            self.OnBlocksReceived(content)
        elif senderAgent.AgentType == AgentType.KinematicsAgent:
            self.Act()
        elif senderAgent.AgentType == AgentType.SupervisorAgent:
            raise NotImplementedError

    def Act(self):
        self.GetBlocks()   

    #internal methods
    def GetBlocks(self):
        self.SendMessage([self._sensorAgent], "DetectBlocks")

    def OnBlocksReceived(self, blocks):
        self.blocks = blocks
        if len(self.blocks) > 0:
            self.SendMessage([self._kinematicsAgent], blocks[0])
        else:
            print "Nisu detekirani blokovi!"

