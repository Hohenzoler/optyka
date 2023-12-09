from classes import game
from gui import gui_main as gui
import pygame
import settingsSetup
from gui import startscreen as ss

settings = settingsSetup.start()

width = settings['WIDTH']
height = settings['HEIGHT']

position = settings['HOTBAR_POSITION']


startscreen = ss.StartScreen(width, height)

settings = settingsSetup.load_settings()

programIcon = pygame.image.load('images/torch.png')

pygame.display.set_icon(programIcon)
game = game.Game(settings)
# light1=light.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
GUI = gui.GUI(game, width, height, position)
game.loop()
