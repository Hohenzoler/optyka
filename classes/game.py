import pygame
from gui import gui
from classes import flashlight


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        # initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.run = True
        self.fps = 60
        self.tick = int((1 / self.fps) * 1000)
        self.mousepos = None  # Mouse position which will be updated every time the mouse is left clicked
        self.rightclickedmousepos = None #right click mouse positon

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousepos = event.pos  # when the left button is clicked the position is saved to self.mousepos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.rightclickedmousepos = event.pos

    def update(self):
        pygame.display.update()
        pygame.time.wait(self.tick)

    def render(self):
        self.screen.fill((0,0,0))
        for object in self.objects:
            object.render()
            if type(self.mousepos) == tuple:
                if type(object) == gui.GUI:  # checks if the class of the object is a gui.GUI
                    object.checkifclicked(self.mousepos)  # if self.mousepos is a tuple it checks if a button has been clicked
                elif type(object) == flashlight.Flashlight:
                    object.checkifclicked(self.mousepos)
            if type(self.rightclickedmousepos) == tuple:
                if type(object) == flashlight.Flashlight:
                    object.selected(self.rightclickedmousepos)

    def background(self):
        self.screen.fill((0, 0, 0))

    def loop(self):
        while self.run:
            self.background()
            self.render()
            self.update()
            self.mousepos = None  # resets self.mouspos
            self.rightclickedmousepos = None
            self.events()
