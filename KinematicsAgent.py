'''
b;40;s1;127;s2;143;s3;90 -> 170,90
b;109;s1;116;s2;155;s3;96 -> 1125,90
b;42;s1;170;s2;54;s3;53; -> 1125,455
b;102;s1;165;s2;66;s3;53 -> 170,455

            'b': [(130, 90, 39),
                 (1145, 90, 125),
                 (130, 620, 46),
                 (1145, 620, 114)],

            's1': [(130, 90, 117),
                 (1145, 90, 105),
                 (130, 620, 165),
                 (1145, 620, 160)],

            's2': [(130, 90, 161),
                 (1145, 90, 174),
                 (130, 620, 73),
                 (1145, 620, 71)],

            's3': [(130, 90, 75),
                 (1145, 90, 80),
                 (130, 620, 74),
                 (1145, 620, 55)],

'''

import time
from Agent import Agent, AgentType
from ControllingAgent import *
from Entities import Manipulator, Block

class KinematicsAgent(Agent):

    def __init__(self, agentType):
        Agent.__init__(self, agentType)

        self._calibration = {
            'b': [(0, 0, 35),
                 (1280, 0, 118),
                 (0, 720, 37),
                 (1280, 720, 115)],

            's1': [(0, 0, 125),
                 (1280, 0, 114),
                 (0, 720, 168),
                 (1280, 720, 163)],

            's2': [(0, 0, 158),
                 (1280, 0, 176),
                 (0, 720, 66),
                 (1280, 720, 77)],

            's3': [(0, 0, 78),
                 (1280, 0, 85),
                 (0, 720, 60),
                 (1280, 720, 60)],
        }

    def AddPeerAgent(self, peerAgent):
        if peerAgent.AgentType == AgentType.LearningAgent:
            self._learningAgent = peerAgent
        elif peerAgent.AgentType == AgentType.ControllingAgent:
            self._controllingAgent = peerAgent

    def SendMessage(self, receivingAgents, content):
        Agent.SendMessage(self, receivingAgents, content) 

    def ReceiveMessage(self, senderAgent, content):
        if senderAgent.AgentType == AgentType.LearningAgent:
            self.MoveBlockToBox(content)
        elif senderAgent.AgentType == AgentType.ControllingAgent:
            self.SendMessage([self._learningAgent], "Done")

    def Act(self):
        print "Act!"

    #internal
    def MoveBlockToBox(self, block):
        print "Pomicem blok " + block.__repr__()

        x = block.Center().x
        y = block.Center().y

        b = self.Interpolate(x,y, self._calibration["b"])
        s1 = self.Interpolate(x,y, self._calibration["s1"])
        s2 = self.Interpolate(x,y, self._calibration["s2"])
        s3 = self.Interpolate(x,y, self._calibration["s3"])
        s4 = block.Angle()

        manipulatorConfig = Manipulator(b,s1,s2,s3,s4,None)
        self.SendMessage([self._controllingAgent], manipulatorConfig)

    def Interpolate(self, x, y, points):
        points = sorted(points)
        (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

        if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
            raise ValueError('points do not form a rectangle')
        if not x1 <= x <= x2 or not y1 <= y <= y2:
            raise ValueError('(x, y) not within the rectangle')

        return abs(int((q11 * (x2 - x) * (y2 - y) + q21 * (x - x1) * (y2 - y) + q12 * (x2 - x) * (y - y1) + q22 * (x - x1) * (y - y1)) / ((x2 - x1) * (y2 - y1) + 0.0)))