import pygame
from gui import gui_main as gui
from gui import settings_screen
from classes import gameobjects
import settingsSetup


class Game:
    def __init__(self):
        self.settings = settingsSetup.load_settings()
        self.width = self.settings['WIDTH']
        self.height = self.settings['HEIGHT']
        self.objects = []
        # initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.fps = 165
        self.tick = int((1 / self.fps) * 1000)
        self.mousepos = None  # Mouse position which will be updated every time the mouse is left clicked
        self.rightclickedmousepos = None  # right click mouse positon
        self.r = False
        self.current_flashlight = None
        self.mode = 'default'
        self.executed_command = 'default'



    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            if self.mode == 'default':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousepos = event.pos  # when the left button is clicked the position is saved to self.mousepos
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.rightclickedmousepos = event.pos
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.r = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        self.r = False

            elif self.mode == 'settings':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for object in self.objects:
                        if type(object) == settings_screen.Settings_screen:
                            object.checkevent(event.pos)


    def update(self):
        pygame.display.update()
        pygame.time.wait(self.tick)

    def render(self):
        if self.mode == 'default':
            # Sort objects based on their layer attribute (assuming you have a layer attribute)
            sorted_objects = sorted(self.objects, key=lambda obj: getattr(obj, 'layer', 0))

            for object in sorted_objects:
                if type(self.mousepos) is tuple:
                    if type(object) is gui.GUI:
                        object.checkifclicked(self.mousepos)
                    elif type(object) is gameobjects.Flashlight:
                        object.checkifclicked(self.mousepos)
                if type(self.rightclickedmousepos) is tuple:
                    if type(object) is gameobjects.Flashlight:
                        object.selected(self.rightclickedmousepos)
                object.render()

        elif self.mode == 'settings':
            if self.executed_command != 'settings':
                self.settings_screen = settings_screen.Settings_screen(self)
                self.settings_screen.render()
                self.executed_command = 'settings'
            else:
                self.settings_screen.render()

        elif self.mode == 'load_new_settings':
            self.objects.remove(self.settings_screen)
            self.settings_screen = None
            self.mode = 'default'

            self.settings = settingsSetup.load_settings()
            self.width = self.settings['WIDTH']
            self.height = self.settings['HEIGHT']
            self.screen = pygame.display.set_mode((self.width, self.height))

            for object in self.objects:
                if type(object) == gui.GUI:
                    object.load_settings()

            self.executed_command = 'default'

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

