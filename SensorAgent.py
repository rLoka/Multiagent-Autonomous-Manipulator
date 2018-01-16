# import the necessary packages
from enum import Enum
import numpy as np
import imutils
import cv2
import time

from Agent import Agent, AgentType
from KinematicsAgent import *
from Entities import Color, Block, Polygon


class SensorAgent(Agent):

    def __init__(self, agentType):
        Agent.__init__(self, agentType)

        self._colorRange = {
            Color.Red: [(0, 200, 0), (3, 255, 255)],
            Color.Green: [(33, 165, 0), (70, 255, 255)],
            Color.Blue: [(100, 130, 0), (130, 255, 255)],
            Color.Yellow: [(20, 115, 180), (80, 255, 255)],
        }

        self._camera = cv2.VideoCapture(1)
        self._camera.set(3, 1280)
        self._camera.set(4, 720)

    def AddPeerAgent(self, peerAgent):
        if peerAgent.AgentType == AgentType.LearningAgent:
            self._learningAgent = peerAgent

    def SendMessage(self, receivingAgents, content):
        Agent.SendMessage(self, receivingAgents, content)

    def ReceiveMessage(self, senderAgent, content):
        if content == "DetectBlocks":
            blocks = self.DetectBlocks()
            self.SendMessage([senderAgent], blocks)

    def Act(self):
        raise NotImplementedError

    # internal methods
    def DetectBlocks(self):
        timeout = time.time() + 60
        blocks = []
        i = 0
        while len(blocks) <= 100:            
            mask = []
            contours = []
            if time.time() > timeout:
                break
            frame = self.GrabFrame()
            i = i + 1
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if(i >= 3):
                for color in self._colorRange:
                    mask = self.ConstructMask(frame, color)
                    contours = self.GetContours(mask)          
                    blocks.extend(self.ConstructBlocks(contours, color))

        return list(set(blocks))

    def GrabFrame(self):
        (grabbed, frame) = self._camera.read()
        return frame

    def ConstructMask(self, frame, color):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self._colorRange[color][0], self._colorRange[color][1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        return mask

    def GetContours(self, mask):
        allContours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        return [c for c in allContours if cv2.contourArea(c) >= 30000]

    def ConstructBlocks(self, contours, color):
        blocks = []
        if len(contours) > 0:
            for c in contours:
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                blocks.append(Block(box, color))
        return blocks