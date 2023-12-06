from classes import game
from gui import gui_main as gui
import pygame
import settingsSetup

settings = settingsSetup.start()

width = int(settings[0])
height = int(settings[1])
position = settings[2]
programIcon = pygame.image.load('images/torch.png')

pygame.display.set_icon(programIcon)
game = game.Game(width, height)
# light1=light.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
GUI = gui.GUI(game, width, height, position)
game.loop()
