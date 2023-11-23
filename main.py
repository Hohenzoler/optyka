from classes import game
from classes import light
from classes import flashlight

objects = [] # creating a objects list that will be drawn to the screen

Flashlight = flashlight.Flashlight(10, 10)

objects.append(Flashlight)

game=game.Game(1000,1000)
light1=light.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
game.loop(objects)