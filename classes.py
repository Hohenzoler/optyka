import pygame
import time
class Game():
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.objects=[]
        #initializing pygame
        pygame.init()
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.run=True
        self.fps=60
        self.tick=int((1/self.fps)*1000)
    def controls(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                self.run=False
    def update(self):
        pygame.display.update()
        pygame.time.wait(self.tick)
    def render(self):
        for object in self.objects:
            object.render()
    def background(self):
        self.screen.fill((0,0,0))
    def loop(self):
        while self.run:
            self.controls()
            self.background()
            self.render()
            self.update()

class Light():
    def __init__(self,game,points,color):
        # points is a list that represents endpoints of next lines building a stream of light
        self.points=points
        self.game=game
        self.color=color
        self.game.objects.append(self)
    def render(self):
        for p in range(0,len(self.points)-1):
            pygame.draw.line(self.game.screen,self.color,self.points[p],self.points[p+1],3)
