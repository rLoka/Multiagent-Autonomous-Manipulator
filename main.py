from Agent import *
from SensorAgent import SensorAgent
from KinematicsAgent import KinematicsAgent
from ControllingAgent import ControllingAgent
from SupervisorAgent import SupervisorAgent
from LearningAgent import LearningAgent

#Agent initialization
sensorAgent = SensorAgent(AgentType.SensorAgent)
kinematicsAgent = KinematicsAgent(AgentType.KinematicsAgent)
controllingAgent = ControllingAgent(AgentType.ControllingAgent)
supervisorAgent = SupervisorAgent(AgentType.SupervisorAgent)
learningAgent = LearningAgent(AgentType.LearningAgent)

#Adding peer agents
#Sensor
sensorAgent.AddPeerAgent(learningAgent)

#Kinematics
kinematicsAgent.AddPeerAgent(learningAgent)
kinematicsAgent.AddPeerAgent(controllingAgent)

#Controlling
controllingAgent.AddPeerAgent(kinematicsAgent)

#Supervisor
supervisorAgent.AddPeerAgent(learningAgent)

#Learning
learningAgent.AddPeerAgent(sensorAgent)
learningAgent.AddPeerAgent(kinematicsAgent)
learningAgent.AddPeerAgent(supervisorAgent)

#Start learning process
learningAgent.Act()