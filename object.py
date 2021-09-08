import numpy as np

class Object:
  def __init__(self):
    self.points = list()

  # points: 개체에 포함할 여러 점들 [[x1, y1, z1], [x2, y2, z2], ...]
  def setPoints(self, *points):
    self.points = points

  # point: 개체에 추가할 점 하나 [xn, yn, zn]
  def addPoint(self, point):
    self.points.append(point)

  # 스크린에 표시할 내용
  def getPoints(self):
    return self.points


class Cube:
  # pos: 정육면체 중앙의 좌표
  # rad: 정육면체에 내접하는 구의 반지름
  def __init__(self, pos, rad):
    self.pos = np.array(pos)
    self.points = [
      self.pos - np.array([  rad,  rad,  rad]),
      self.pos - np.array([ -rad,  rad,  rad]),
      self.pos + np.array([  rad, -rad,  rad]),
      self.pos - np.array([  rad,  rad, -rad]),

      self.pos + np.array([  rad,  rad,  rad]),
      self.pos + np.array([ -rad,  rad,  rad]),
      self.pos - np.array([  rad, -rad,  rad]),
      self.pos + np.array([  rad,  rad, -rad])
    ]

    self.planes = [
      [self.points[0], self.points[1], self.points[2], self.points[3]],
      [self.points[0], self.points[1], self.points[7], self.points[6]],
      [self.points[0], self.points[3], self.points[5], self.points[6]],
      [self.points[4], self.points[2], self.points[1], self.points[7]],
      [self.points[4], self.points[7], self.points[6], self.points[5]],
      [self.points[4], self.points[2], self.points[3], self.points[5]]
    ]

  def getPoints(self):
    return self.points

  def getPlanes(self):
    return self.planes