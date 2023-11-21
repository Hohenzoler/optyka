import classes
game=classes.Game(500,500)
light1=classes.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
game.loop()