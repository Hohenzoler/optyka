import pygame
from gui import gui
from classes import gameobjects


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        # initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.run = True
        self.fps = 120
        self.tick = int((1 / self.fps) * 1000)
        self.mousepos = None  # Mouse position which will be updated every time the mouse is left clicked
        self.rightclickedmousepos = None  # right click mouse positon
        self.r=False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousepos = event.pos  # when the left button is clicked the position is saved to self.mousepos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.rightclickedmousepos = event.pos
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    self.r=True
            elif event.type == pygame.KEYUP:
                if event.key==pygame.K_r:
                    self.r=False

    def update(self):
        pygame.display.update()
        pygame.time.wait(self.tick)

    def render(self):
        # Sort objects based on their layer attribute (assuming you have a layer attribute)
        sorted_objects = sorted(self.objects, key=lambda obj: getattr(obj, 'layer', 0))

        for object in sorted_objects:
            if type(self.mousepos) is tuple:
                if type(object) is gui.GUI:
                    object.checkifclicked(self.mousepos)
                elif type(object) is gameobjects.Flashlight:
                    object.checkifclicked(self.mousepos)

        for object in sorted_objects:
            object.render()

            if type(self.rightclickedmousepos) is tuple:
                if type(object) is gameobjects.Flashlight:
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

