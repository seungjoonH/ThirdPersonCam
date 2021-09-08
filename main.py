import math as m
from object import *
import pygame as pg
import numpy as np
from camera import Camera

pg.init()

# setting
clock = pg.time.Clock()
FPS = 60

# color
WHITE = [ 255, 255, 255]
BLACK = [   0,   0,   0]
RED   = [ 255,   0,   0]
GREEN = [   0, 255,   0]
BLUE  = [   0,   0, 255]

# screen
# size = [1280, 720]
size = [700, 700]
screen = pg.display.set_mode(size)

title = '3D Camera'
pg.display.set_caption(title)

# camera
viewPoint = np.array([3., 3., 3.])
viewingAngle = (30, 30)
sightVector = np.array([])
angularVelocity = 2
rotatedVector = np.identity(3)

def setSightVector():
  global viewPoint, sightVector
  sightVector = -np.array(viewPoint) * 2/5

setSightVector()

camera = Camera(viewPoint, viewingAngle, sightVector)

# global variable
WIDTH = float()
HEIGHT = float()

HT = np.array([])
HR = np.array([])

X = np.array([])
Y = np.array([])
Z = np.array([])

HX = np.array([])
HY = np.array([])
HZ = np.array([])

def PtoHPP(P):
  global viewPoint, sightVector, rotatedVector
  rotP = rotatedVector * np.transpose(np.matrix(P))
  rotP = np.transpose(rotP)
  prop = float(np.linalg.norm(sightVector) / (camera.unit(sightVector) * np.transpose(np.matrix(rotP - viewPoint))))

  if prop > 1:
    return 'escape'#np.array(rotP-viewPoint)[0]

  VPP = prop * (rotP - viewPoint)
  HPP = VPP - sightVector
  HPP = np.array(HPP)[0]
  for i in range(len(HPP)):
    HPP[i] = round(HPP[i], 10)
  return HPP

def HPPtoCoords(HPP):
  if str(HPP) == 'escape': return HPP
  global rotatedVector, HT, HR
  coords = np.array([np.dot(HPP, HR), np.dot(HPP, HT)])
  return coords

def coordsToScreen(pos):
  if str(pos) == 'escape': return pos
  global WIDTH, HEIGHT
  scaleX = size[0] / WIDTH
  scaleY = size[1] / HEIGHT
  x = pos[0] * scaleX + size[0] / 2; y = -pos[1] * scaleY + size[1] / 2
  return x, y

def dot(color, pos):
  if str(pos) == 'escape': return 
  srcPos = coordsToScreen(pos)
  pg.draw.circle(screen, color, srcPos, 3)

def line(color, pos1, pos2):
  if str(pos1) == 'escape': return 
  if str(pos2) == 'escape': return 
  srcPos1 = coordsToScreen(pos1)
  srcPos2 = coordsToScreen(pos2)
  pg.draw.line(screen, color, srcPos1, srcPos2, 1)

def poly(color, *poses):
  srcPoses = list()
  for pos in poses[0]:
    if str(pos) != 'escape': srcPoses.append(coordsToScreen(pos))
  if len(srcPoses) > 1:
    pg.draw.lines(screen, color, True, srcPoses, 1)

def drawAxis(len):
  O = HPPtoCoords(PtoHPP([0, 0, 0]))
  X = HPPtoCoords(PtoHPP([len, 0, 0]))
  Y = HPPtoCoords(PtoHPP([0, len, 0]))
  Z = HPPtoCoords(PtoHPP([0, 0, len]))
  
  line(RED, O, X)
  line(GREEN, O, Y)
  line(BLUE, O, Z)

def rotAxis(axis, vec, th):
  uT = np.matrix(axis)
  u = np.transpose(uT)
  I = np.identity(3)
  x, y, z = tuple(np.array(u)[0])
  mtx = np.matrix([
    [0, -z, y],
    [z, 0, -x],
    [-y, x, 0]
  ])
  retVec = (mtx * m.sin(th) + (I - u * uT) * m.cos(th) + u * uT) * vec
  return np.linalg.norm(vec) * camera.unit(retVec)

def rotXaxis(vec, th):
  global rotatedVector
  Xaxis = np.transpose(np.matrix([1, 0, 0]))
  Xaxis = rotatedVector * Xaxis
  return rotAxis(Xaxis, vec, th)

def rotYaxis(vec, th):
  global rotatedVector
  Yaxis = np.transpose(np.matrix([0, 1, 0]))
  Yaxis = rotatedVector * Yaxis
  return rotAxis(Yaxis, vec, th)

def rotZaxis(vec, th):
  global rotatedVector
  Zaxis = np.transpose(np.matrix([0, 0, 1]))
  Zaxis = rotatedVector * Zaxis
  return rotAxis(Zaxis, vec, th)

def rotX(th):
  global rotatedVector
  rotatedVector = rotXaxis(rotatedVector, th)

def rotY(th):
  global rotatedVector
  rotatedVector = rotYaxis(rotatedVector, th)

def rotZ(th):
  global rotatedVector
  rotatedVector = rotZaxis(rotatedVector, th)

running = True
while running:
    mouse_pos = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
              running = False

    pressed = pg.key.get_pressed()
    if pressed[pg.K_q]: rotX(.01 * angularVelocity)
    if pressed[pg.K_w]: rotX(-.01 * angularVelocity)
    if pressed[pg.K_a]: rotY(.01 * angularVelocity)
    if pressed[pg.K_s]: rotY(-.01 * angularVelocity)
    if pressed[pg.K_z]: rotZ(.01 * angularVelocity)
    if pressed[pg.K_x]: rotZ(-.01 * angularVelocity)

    screen.fill(BLACK)
    
    HT = camera.HT
    HR = camera.HR

    # X = camera.X
    # Y = camera.Y
    # Z = camera.Z

    # HX = camera.HX
    # HY = camera.HY
    # HZ = camera.HZ
    
    WIDTH = camera.width
    HEIGHT = camera.height

    # camera.V = viewPoint; camera.S = sightVector
    # camera.HT = HT; camera.HR = HR

    # camera.X = X; camera.Y = Y; camera.Z = Z
    # camera.HX = HX; camera.HY = HY; camera.HZ = HZ
    # print(viewPoint, sightVector)

    drawAxis(2)

    PsCube = Cube([.5, .5, .5], .5)
    Ps = PsCube.getPlanes()
    
    for p in Ps:
      tp = list()
      for e in p:
        tp.append(HPPtoCoords(PtoHPP(e)))
      poly(WHITE, tp)

    # update screen
    clock.tick(FPS)
    pg.display.flip()

pg.quit()