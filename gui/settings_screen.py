import pygame
from gui import button
from gui import dropdown_menu as dm
from classes import sounds

class Settings_screen:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen

        self.objects = []

        self.dimentions = [{'WIDTH': 2560, 'HEIGHT': 1440}, {'WIDTH': 1920, 'HEIGHT': 1080},
                           {'WIDTH': 1280, 'HEIGHT': 720}, {'WIDTH': 1000, 'HEIGHT': 700}]
        self.HopbarPositions = ['Bottom', 'Top', 'Left', 'Right']

        self.Fullscreen = [{'FULLSCREEN': 'ON'}, {'FULLSCREEN': 'OFF'}]

        self.font2 = pygame.font.Font('freesansbold.ttf', self.width // 40)

        self.font = pygame.font.Font('freesansbold.ttf', self.width // 20)

        self.maintext = self.font.render('Settings', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width // 2, (self.height // 2) - (3 * self.height // 10))

        self.resolutiontext = self.font2.render('Resolution:', True, 'white')
        self.resolutiontextRect = self.resolutiontext.get_rect()
        self.resolutiontextRect.center = (
        self.width // 2 - self.width // 10, self.height // 2 - 2 * (self.height // 20 + self.height // 47))

        self.FStext = self.font2.render('Fullscreen:', True, 'white')
        self.FStextRect = self.FStext.get_rect()
        self.FStextRect.center = (
        self.width // 2 - self.width // 10, self.height // 2 - (self.height // 27 + self.height // 47))

        self.hoptext = self.font2.render('Hopbar location:', True, 'white')
        self.hoptextRect = self.hoptext.get_rect()

        self.hoptextRect.center = (self.width // 2 - self.width // 10, self.height // 2 + (self.height // 50 + self.height // 47))

        save_n_exit = button.ButtonForgame(71, self)

        self.DropdownMenus = []

        self.DropdownMenus = [dm.DropdownMenu(self, x) for x in range(3)]

        self.game.objects.append(self)


    def render(self):
        self.screen.blit(self.resolutiontext, self.resolutiontextRect)
        self.screen.blit(self.hoptext, self.hoptextRect)
        self.screen.blit(self.maintext, self.maintextRect)
        self.screen.blit(self.FStext, self.FStextRect)

        for object in self.objects:
            object.render()

    def checkevent(self, pos):
        for object in self.objects:
            object.checkcollision(pos)




