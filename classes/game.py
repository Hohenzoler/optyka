import pygame
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
    def loop(self, objects):
        while self.run:
            self.controls()
            self.background()
            self.render()
            for object in objects:  #drawing objects from the objects list that have .draw() function
                object.draw(self.screen)
            self.update()