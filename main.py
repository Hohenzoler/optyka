from classes import game
from gui import gui

width = 1000
height = 700

game = game.Game(width, height)
# light1=light.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
GUI = gui.GUI(game, width, height)
game.loop()
