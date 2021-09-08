import numpy as np
import math as m
from object import *

class Camera:
  # viewpoint: 시점의 좌표 [v1, v2, v3]
  # viewingAngle: 시야각 (thetaX, thetaY)
  # sightVector: 시야벡터 [0, 0, 1] (가변적); vector VH
  def __init__(self, viewPoint, viewingAngle, sightVector):
    self.V = np.array(viewPoint) 
    self.normV = np.linalg.norm(self.V)
    self.aX = m.radians(viewingAngle[0])
    self.aY = m.radians(viewingAngle[1])
    self.S = np.array(sightVector)
    self.unitS = Camera.unit(self.S) # S 단위벡터

    self.H = self.V + self.S
    Hx, Hy, Hz = self.H

    # support function: x * sqrt(1 / (x ** 2 + y ** 2))
    def sp(p, q):
      return p * m.sqrt(1 / (p ** 2 + q ** 2))

    # 시계반대방향
    self.HX = np.array([0, -sp(Hz, Hy), sp(Hy, Hz)])
    self.HY = np.array([sp(Hz, Hx), 0, -sp(Hx, Hz)])
    self.HZ = np.array([-sp(Hy, Hx), sp(Hx, Hy), 0])

    # std = {'x': [self.V[0], 0, 0], 'y': [0, self.V[1], 0], 'z': [0, 0, self.V[2]]}
    # rX = self.H - std['x']; rY = self.H - std['y']; rZ = self.H - std['z']
    # self.HX = np.cross(std['x'], rX) / np.linalg.norm(np.cross(std['x'], rX))
    # self.HY = np.cross(std['y'], rY) / np.linalg.norm(np.cross(std['y'], rY))
    # self.HZ = np.cross(std['z'], rZ) / np.linalg.norm(np.cross(std['z'], rZ))

    self.X = self.H + self.HX
    self.Y = self.H + self.HY
    self.Z = self.H + self.HZ

    self.HT = np.array([0., 1., 0.])#Camera.unit(self.HZ - self.HX)
    self.HR = self.HY

    self.T = self.H + self.HT
    self.R = self.H + self.HR

    self.width = 2 * np.linalg.norm(self.S) * m.tan(self.aX)
    self.height = 2 * np.linalg.norm(self.S) * m.tan(self.aY)
    
  
  @staticmethod
  def unit(vec):
    return np.matrix(vec) / np.linalg.norm(vec)

  @staticmethod
  def isParallel(vec1, vec2):
    rat = [0, 0, 0]
    for i in range(3):
      if vec2[i]: rat[i] = vec1[i] / vec2[i]
      else: rat[i] = 0

    return rat[0] == rat[1] == rat[2]

  @staticmethod
  def findPHI(V, P, S):
    VP = P - V
    normVP = np.linalg.norm(VP)
    normS = np.linalg.norm(S)
    return m.acos(np.dot(S, P) / normVP / normS)

  def update(self, viewPoint, viewingAngle, sightVector):
    self.__init__(viewPoint, viewingAngle, sightVector)


# Camera([5, 5, 5], (60, 40), [-1, -1, -1])