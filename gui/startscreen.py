import pygame
from gui import button
from gui import dropdown_menu as dm
import settingsSetup


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
        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width//2, (self.height//2) - 200)

        self.executed_functions = 'default'


        self.dimentions = [{'WIDTH': 2560, 'HEIGHT': 1440}, {'WIDTH': 1920, 'HEIGHT': 1080}, {'WIDTH': 1280, 'HEIGHT': 720}, {'WIDTH': 1000, 'HEIGHT': 700}]


        self.buttons = [button.ButtonForStartScreen(x, self) for x in range(3)]

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
                    if type(object) == button.ButtonForStartScreen:
                        object.checkcollision(event.pos)
                    elif type(object) == dm.DropdownMenu:
                        object.handle_event(event)

    def render(self):
        self.screen.fill('black')
        for object in self.objects:
            object.render()

        self.screen.blit(self.maintext, self.maintextRect)
        pygame.display.update()

    def defualt_mode(self):
        if self.executed_functions != 'default':
            self.buttons = [button.ButtonForStartScreen(x, self) for x in range(3)]
            self.executed_functions = 'default'
            pygame.display.update()

    def settings_mode(self):
        if self.executed_functions != 'settings':
            self.buttons = []

            for object in self.objects:
                if type(object) == button.ButtonForStartScreen:
                    self.objects.remove(object)

            for object in self.objects:
                if type(object) == button.ButtonForStartScreen:
                    self.objects.remove(object)


            self.DropdownMenus = [dm.DropdownMenu(self, x) for x in range(1)]

            save_n_exit = button.ButtonForStartScreen(71, self)

            self.buttons.append(save_n_exit)
            print(self.buttons[0])

            self.executed_functions = 'settings'

    def load_new_settings(self):

        self.buttons = []

        for object in self.objects:
            if type(object) == button.ButtonForStartScreen:
                self.objects.remove(object)
            elif type(object) == dm.DropdownMenu:
                self.objects.remove(object)

        for object in self.objects:
            if type(object) == button.ButtonForStartScreen:
                self.objects.remove(object)
            elif type(object) == dm.DropdownMenu:
                self.objects.remove(object)


        settings = settingsSetup.load_settings()

        self.width = settings['WIDTH']
        self.height = settings['HEIGHT']

        self.font = pygame.font.Font('freesansbold.ttf', self.width // 20)
        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width // 2, (self.height // 2) - 200)

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.mode = 'default'







