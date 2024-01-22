import pygame
import math

import classes.gameobjects
from classes import gameobjects, fps
import gui
from gui.button import *
import time
import functions

currentPoints = []
def addPoint(mousePos):
    print('point added')
    currentPoints.append(mousePos)