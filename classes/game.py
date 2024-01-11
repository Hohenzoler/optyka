import pygame
from gui import gui_main as gui
from gui import settings_screen
from classes import gameobjects
import settingsSetup
from classes import fps
from classes import bin


class Game:
    def __init__(self):
        self.settings = settingsSetup.load_settings()
        self.width = self.settings['WIDTH']
        self.height = self.settings['HEIGHT']
        self.font = pygame.font.Font(None, self.height//20)
        self.objects = []
        # initializing pygame
        pygame.init()
        if self.settings['FULLSCREEN'] == 'ON':
        #     if self.settings['VSYNC'] == 'ON':
        #         self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=1)
        #     else:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=0)
        else:
            # if self.settings['VSYNC'] == 'ON':
            #     self.screen = pygame.display.set_mode((self.width, self.height), vsync=1)
            # else:
                self.screen = pygame.display.set_mode((self.width, self.height), vsync=0)
        self.run = True
        self.fps = fps.return_fps()

        self.tick = int((1 / self.fps) * 1000)
        self.mousepos = None  # Mouse position which will be updated every time the mouse is left clicked
        self.rightclickedmousepos = None  # right click mouse positon
        self.r = False
        self.current_flashlight = None
        self.mode = 'default'
        self.executed_command = 'default'

        self.clock = pygame.time.Clock()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            if self.mode == 'default':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousepos = event.pos  # when the left button is clicked the position is saved to self.mousepos
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.rightclickedmousepos = event.pos
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.r = 10
                    if event.y < 0:
                        self.r = -10

            elif self.mode == 'settings':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for object in self.objects:
                        if type(object) == settings_screen.Settings_screen:
                            object.checkevent(event.pos)


    def update(self):
        pygame.display.update()
        self.clock.tick(self.fps)

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
                    elif type(object) is gameobjects.Mirror:
                        object.checkifclicked(self.mousepos)
                if type(self.rightclickedmousepos) is tuple:
                    if type(object) is gameobjects.Flashlight:
                        object.selected(self.rightclickedmousepos)
                    if type(object) is gameobjects.Mirror:
                        object.selected(self.rightclickedmousepos)
                object.render()

                if type(object) != bin.Bin:
                    for bin_2 in self.objects:
                        if type(bin_2) == bin.Bin:
                            bin_2.checkCollision(object)
                            break

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

            if self.settings['FULLSCREEN'] == 'ON':
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((self.width, self.height))

            for object in self.objects:
                if type(object) == gui.GUI or type(object) == bin.Bin:
                    object.load_settings()

            self.executed_command = 'default'

        self.displayFPS()

    def background(self):
        self.screen.fill((0, 0, 0))


    def displayFPS(self):
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", True, "white")
        self.screen.blit(fps_text, (10, 10))

    def loop(self):
        while self.run:
            self.background()
            self.render()
            self.update()
            self.mousepos = None  # resets self.mouspos
            self.rightclickedmousepos = None
            self.events()

