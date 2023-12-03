# game.py
import pygame
from classes.gameobjects import Flashlight, GameObject
from gui.gui import GUI

class Game:
    # Main game class
    def __init__(self, width, height):
        # Initialize the game
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

    def events(self):
        # Handle game events
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
        # Update the game
        pygame.display.update()
        pygame.time.wait(self.tick)

    def render(self):
        # Render game objects
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
        # Set the background color
        self.screen.fill((0, 0, 0))

    def loop(self):
        # Main game loop
        while self.run:
            self.background()
            self.render()
            self.update()
            self.mousepos = None
            self.rightclickedmousepos = None
            self.events()
