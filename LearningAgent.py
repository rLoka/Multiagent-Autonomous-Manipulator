import time
import serial
import random
import numbers

from Agent import Agent, AgentType
from Entities import Color

class LearningAgent(Agent):
    def __init__(self, agentType):
        Agent.__init__(self, agentType)

        self.R = [
            [None,  Color.Initial, Color.Green, Color.Yellow, Color.Blue, Color.Red],
            [Color.Initial, None, 10, -1, -1, -1],
            [Color.Green,  None, None, -1, 10, -1],
            [Color.Yellow, None, -1, None, -1, -1],
            [Color.Blue, None, -1, -1, None, 10],
            [Color.Red, None, -1, 10, -1, None]
        ]

        self.Q = [
            [None,  Color.Initial, Color.Green, Color.Yellow, Color.Blue, Color.Red],
            [Color.Initial, None, 0, 0, 0, 0],
            [Color.Green,  None, None, 0, 0, 0],
            [Color.Yellow, None, 0, None, 0, 0],
            [Color.Blue, None, 0, 0, None, 0],
            [Color.Red, None, 0, 0, 0, None]
        ]

        self.g = 0.8
        self.l = 1.0
        self.e = 1.0
        self.i = 0


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
            self.GetBlocks()
        elif senderAgent.AgentType == AgentType.SupervisorAgent:
            raise NotImplementedError

    def Act(self):
        self.StartEpisode()

    #internal methods
    def StartEpisode(self):
        if not self.IsFinalState():
            self.i = self.i + 1
            self.e = self.e * 0.75
            self.l = self.l * 0.75

            self.availableStates = [Color.Initial, Color.Green, Color.Yellow, Color.Blue, Color.Red]

            self.previousState = Color.Initial
            self.currentState = Color.Initial   

            self.currentAction = {"index" : 1, "value" : self.Q[1][1], "state": Color.Initial}
            self.GetBlocks()
        else:
            print "Pronaden je optimalni redoslijed!"
            print self.Q    

    def Learn(self, blocks):
        if len(self.availableStates) > 1:
            if set([b.Color for b in blocks]) != set([s for s in self.availableStates if s != Color.Initial]):
                print "Nisu detekirani svi potrebni blokovi!"
                answer = raw_input("Zelite li ponovno skenirati? (y/n): ")
                if answer == 'y\r':
                    self.SendMessage([self._sensorAgent], "DetectBlocks")
                    return
                else:
                    print self.Q
                    return

            self.availableStates.remove(self.currentState)
            self.availableActions = self.GetAvalaibleActionsForState(self.GetStateIndex(self.currentState), self.availableStates)

            if random.uniform(0, 1) < self.e:
                self.currentAction = random.choice(self.availableActions)
            else:
                self.currentAction = max(self.availableActions, key=lambda a:a['value'])
            
            for b in blocks:
                if b.Color == self.currentAction["state"]:
                    self.SendMessage([self._kinematicsAgent], b)

            self.currentState = self.currentAction["state"]
            rewardForAction = self.R[self.GetStateIndex(self.previousState)][self.currentAction["index"]]

            self.Q[self.GetStateIndex(self.previousState)][self.currentAction["index"]] = self.l * (rewardForAction + self.g * self.GetMaxActionForState(self.currentState)["value"]) + (1 - self.l) * self.Q[self.GetStateIndex(self.previousState)][self.currentAction["index"]]
                            
            self.previousState = self.currentState
        
        else:
            self.StartEpisode()


    def GetBlocks(self):
        self.SendMessage([self._sensorAgent], "DetectBlocks")

    def OnBlocksReceived(self, blocks):
        self.Learn(blocks)


    def IsFinalState(self):
        if (
            self.GetMaxActionForState(Color.Initial)["state"] == Color.Green and
            self.GetMaxActionForState(Color.Green)["state"] == Color.Blue and
            self.GetMaxActionForState(Color.Red)["state"] == Color.Yellow and
            self.GetMaxActionForState(Color.Blue)["state"] == Color.Red    
        ):
            return True
        else:
            return False

    def GetAllActionsForState(self, state):
        row = self.Q[self.GetStateIndex(state)]

        availableActions = []

        for i in range(0, len(row)):
            if isinstance(row[i], numbers.Number):
                availableActions.append({"index" : i, "value" : row[i], "state": self.Q[0][i]})

        return availableActions

    def GetAvalaibleActionsForState(self, stateIndex, availableStates):
        availableStatesIndexes = [self.Q[0].index(s) for s in availableStates]
        row = self.Q[stateIndex]

        availableActions = []

        for i in range(0, len(row)):
            if isinstance(row[i], numbers.Number) and i in availableStatesIndexes:
                availableActions.append({"index" : i, "value" : row[i], "state": self.Q[0][i]})

        return availableActions

    def GetStateIndex(self, state):
        return self.Q[0].index(state)

    def GetMaxActionForState(self, state):
        return max(self.GetAllActionsForState(state), key=lambda a:a['value'])