import pygame
from pygame import draw
import math
import classes.game
import classes.gameobjects
from classes import gameobjects, fps
import gui
from gui.button import *
import time

class polygonDrawing:

    def __init__(self):
        self.currentPolygonPoints = []


    def addPoint(self, mousePos):
        self.currentPolygonPoints.append(mousePos)

        print(self.currentPolygonPoints)
    # def renderDots():
    #     for i in currentPolygonPoints:
    #         pygame.draw.circle(screen, (200, 200, 200), i, 10)
    def clearPoints(self):
        self.currentPolygonPoints = []
    def createPolygon(self, game):
        if len(self.currentPolygonPoints) >= 3:
            Adam = gameobjects.Mirror(game, self.currentPolygonPoints, (200, 0, 0), 0, 1, 0)
            game.objects.append(Adam)
            self.clearPoints()

    def returnPolygonPoints(self):
        return self.currentPolygonPoints

