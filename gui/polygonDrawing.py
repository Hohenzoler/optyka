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
def clearPoints():
    global currentPolygonPoints
    currentPolygonPoints = []
def createPolygon(game):
    global currentPolygonPoints
    if len(currentPolygonPoints) >= 3:
        Adam = gameobjects.Mirror(game, currentPolygonPoints, (200, 0, 0), 0, 1, 1)
        game.objects.append(Adam)
        clearPoints()

