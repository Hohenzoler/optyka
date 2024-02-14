import pygame
from pygame import draw
import math
import classes.game
import classes.gameobjects
from classes import gameobjects, fps
import gui
from gui.button import *
import time

currentPolygonPoints = []
def addPoint(mousePos):
    currentPolygonPoints.append(mousePos)

    print(currentPolygonPoints)
# def renderDots():
#     for i in currentPolygonPoints:
#         pygame.draw.circle(screen, (200, 200, 200), i, 10)

def createPolygon(game):
    if len(currentPolygonPoints) >= 3:
        print(1345)
        thisOnesPoints = currentPolygonPoints
        Adam = gameobjects.Mirror(game, thisOnesPoints, (200, 0, 0), 0, 0.4, 0.6)
        game.objects.append(Adam)
        # currentPolygonPoints.clear()

    else:
        pass