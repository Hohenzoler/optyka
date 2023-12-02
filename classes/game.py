import pygame

from classes.gameobjects import Flashlight, GameObject
from gui import gui
from classes import gameobjects
from gui.gui import GUI


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []  # Ensure that this list contains instances of GUI and other game objects
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.run = True
        self.fps = 120
        self.tick = int((1 / self.fps) * 1000)
        self.mousepos = None
        self.rightclickedmousepos = None
        self.r = False

        # Add GUI instance to the objects list
        self.objects.append(GUI(self, self.width, self.height))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousepos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.rightclickedmousepos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.r = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.r = False

    def update(self):
        pygame.display.update()
        pygame.time.wait(self.tick)

    def render(self):
        sorted_objects = sorted(self.objects, key=lambda obj: getattr(obj, 'layer', 0))

        for obj in sorted_objects:
            if type(self.mousepos) is tuple:
                if type(obj) is GUI:
                    obj.checkifclicked(self.mousepos)
                elif type(obj) is Flashlight:
                    obj.checkifclicked(self.mousepos)

        for obj in sorted_objects:
            obj.render()

            if type(self.rightclickedmousepos) is tuple:
                if type(obj) is Flashlight:
                    obj.selected(self.rightclickedmousepos)


    def background(self):
        self.screen.fill((0, 0, 0))

    def loop(self):
        while self.run:
            self.background()
            self.render()
            self.update()
            self.mousepos = None
            self.rightclickedmousepos = None
            self.events()
