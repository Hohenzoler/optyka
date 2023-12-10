import pygame
from gui import button
import settingsSetup
from gui import settings_screen


pygame.init()

class StartScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.run = True
        self.mode = 'default'
        self.objects = []
        self.font = pygame.font.Font('freesansbold.ttf', self.width//20)


        self.executed_functions = 'default'

        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width // 2, (self.height // 2) - (3 * self.height // 10))

        self.buttons = [button.ButtonForgame(x, self) for x in range(3)]

        pygame.display.set_caption('Optyka')

        self.mainloop()


    def mainloop(self):
        while self.run:
            if self.mode == 'default':
                self.defualt_mode()

            elif self.mode == 'settings':
                self.settings_mode()

            elif self.mode == 'load_new_settings':
                self.load_new_settings()

            self.checkforevents()
            self.render()

    def checkforevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for object in self.objects:
                    if type(object) == button.ButtonForgame:
                        object.checkcollision(event.pos)
                    elif type(object) == settings_screen.Settings_screen:
                        object.checkevent(event.pos)

    def render(self):
        self.screen.fill('black')
        for object in self.objects:
            object.render()

        self.screen.blit(self.maintext, self.maintextRect)


        pygame.display.update()

    def defualt_mode(self):
        if self.executed_functions != 'default':
            self.buttons = [button.ButtonForgame(x, self) for x in range(3)]
            self.executed_functions = 'default'

    def settings_mode(self):
        if self.executed_functions != 'settings':
            self.buttons = []

            for object in self.objects:
                if type(object) == button.ButtonForgame:
                    self.objects.remove(object)

            for object in self.objects:
                if type(object) == button.ButtonForgame:
                    self.objects.remove(object)

            self.settingsscreen = settings_screen.Settings_screen(self)

            self.executed_functions = 'settings'

    def load_new_settings(self):

        self.objects.remove(self.settingsscreen)

        for object in self.objects:
            if type(object) == button.ButtonForgame:
                self.objects.remove(object)

        for object in self.objects:
            if type(object) == button.ButtonForgame:
                self.objects.remove(object)
            elif type(object) == dm.DropdownMenu:
                self.objects.remove(object)

        for object in self.objects:
            if type(object) == button.ButtonForgame:
                self.objects.remove(object)
            elif type(object) == dm.DropdownMenu:
                self.objects.remove(object)



        settings = settingsSetup.load_settings()

        self.width = settings['WIDTH']
        self.height = settings['HEIGHT']

        self.font = pygame.font.Font('freesansbold.ttf', self.width // 20)
        self.font2 = pygame.font.Font('freesansbold.ttf', self.width // 40)
        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width//2, (self.height//2) - (3 * self.height//10))

        self.resolutiontext = self.font2.render('Resolution:', True, 'white')
        self.resolutiontextRect = self.resolutiontext.get_rect()
        self.resolutiontextRect.center = (
        self.width // 2 - self.width // 10, self.height // 2 - 2 * (self.height // 20 + self.height // 47))

        self.hoptext = self.font2.render('Hopbar location:', True, 'white')
        self.hoptextRect = self.hoptext.get_rect()
        self.hoptextRect.center = (
        self.width // 2 - self.width // 10, self.height // 2 - (self.height // 20 + self.height // 47))

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.mode = 'default'
