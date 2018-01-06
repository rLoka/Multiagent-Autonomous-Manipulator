from enum import Enum
import serial

class AgentType(Enum):
    ControllerAgent = 0
    KinematicsAgent = 1
    SensorAgent = 2
    LearningAgent = 3

class Agent:

    def __init__(self, agentType):
        self.AgentType = agentType
        self.PeerAgents = []

    def AddPeerAgent(self, peerAgent):
        self.PeerAgents.append(peerAgent)
        self.OnPeerAgentAdded()

    def OnPeerAgentAdded(self):
        raise NotImplementedError

    def SendMessage(self, receivingAgents, content):
        for agent in receivingAgents:
            agent.ReceiveMessage(self, content)

    def ReceiveMessage(self, senderAgent, content):
        raise NotImplementedError

    def Act(self):
        raise NotImplementedError
    
    def Stop(self):
        raise NotImplementedError