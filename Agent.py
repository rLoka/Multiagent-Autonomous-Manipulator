from enum import Enum

class AgentType(Enum):
    ControllingAgent = 0
    KinematicsAgent = 1
    SensorAgent = 2
    LearningAgent = 3
    SupervisorAgent = 4

class Agent:

    def __init__(self, agentType):
        self.AgentType = agentType
        self.PeerAgents = []

    def AddPeerAgent(self, peerAgent):
        raise NotImplementedError

    def SendMessage(self, receivingAgents, content):
        for agent in receivingAgents:
            agent.ReceiveMessage(self, content)

    def ReceiveMessage(self, senderAgent, content):
        raise NotImplementedError

    def Act(self):
        raise NotImplementedError