import game
import light

game=game.Game(1000,1000)
light1=light.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
game.loop()