from classes import game
from gui import gui_main as gui
import pygame
import settingsSetup
from gui import startscreen as ss

settings = settingsSetup.start()

# print(settings)

width = settings['WIDTH']
height = settings['HEIGHT']

position = settings['HOPBAR_POSITION']

programIcon = pygame.image.load('images/torch_icon.png')

pygame.display.set_icon(programIcon)

startscreen = ss.StartScreen(width, height)


game = game.Game()
# light1=light.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
GUI = gui.GUI(game)
# print(pygame.display.Info())
game.loop()
