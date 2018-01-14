from enum import Enum
from sympy import Point, Line, Segment
import math


class Color(Enum):
    Red = "crvena"
    Green = "zelena"
    Blue = "plava"
    Yellow = "zuta"

class Block:
    def __init__(self, box, color):
        self.Box = box
        self.Color = color
        self.Polygon = None

    def __hash__(self):
        return hash(self.Color)

    def __eq__(self, other):
        return self.Color == other.Color

    def __repr__(self):
        return str(str(self.Color.value) + ", (" + str(int(self.Center().x)) + "," + str(int(self.Center().y)) + "), " + str(self.Angle()))

    def Center(self):
        return Segment(Point(self.Box[0][0], self.Box[0][1]), Point(self.Box[2][0], self.Box[2][1])).midpoint

    def Angle(self):
        yAxis = Line(Point(0,1), Point(0,0))
        point1 = Point(self.Box[1][0], self.Box[1][1])
        point2 = Point(self.Box[0][0], self.Box[0][1])
        point3 = Point(self.Box[2][0], self.Box[2][1])

        if point1.distance(point2) > point1.distance(point3):
            longerLine = Line(point1, point2)
        else:
            longerLine = Line(point1, point3)

        angle = int(math.degrees(yAxis.angle_between(longerLine)))

        if (int(angle) > 90):
            if angle - 180 + 80 >= 0:
                return angle - 180 + 80
            else:   
                return 0
        else:
            if angle + 80 >= 0:
                return angle + 80
            else:   
                return 0
    
    def SetPolygon(self, polygon):
        self.polygon = polygon


class Polygon:
    def __init__(self, x, y, angle, color):        
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.blocks = []
    
    def AddBlock(self, block):
        self.blocks.append(block)

class Manipulator:
    def __init__(self, base, shaft1, shaft2, shaft3, shaft4, tool):        
        self.Base = base
        self.Shaft1 = shaft1
        self.Shaft2 = shaft2
        self.Shaft3 = shaft3
        self.Shaft4 = shaft4
        self.Tool = tool
    
    def ToText(self):
        return  str("b;" + str(self.Base) + ";s1;"+ str(self.Shaft1) + ";s2;" + str(self.Shaft2) + ";s3;" + str(self.Shaft3) + ";s4;" + str(self.Shaft4) + ";" + "t;154;").strip('"\'')