import pygame
from pygame import draw
import math

import classes.gameobjects
from classes import gameobjects, fps
import gui
from gui.button import *
import time
import functions

currentPolygonPoints = []
def addPoint(mousePos):
    currentPolygonPoints.append(mousePos)

    print(currentPolygonPoints)
def renderDots():
    for i in currentPolygonPoints:
        pygame.draw.circle(screen, (200, 200, 200), i, 10)

def createPolygon():
    if len(currentPolygonPoints) >= 3:
        print(1345)
        Adam = gameobjects.GameObject(game, currentPolygonPoints, (200, 0, 0), None, None)
    currentPolygonPoints.clear()