import pygame
from gui import button
from gui import dropdown_menu as dm
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

        self.font2 = pygame.font.Font('freesansbold.ttf', self.width // 40)

        self.resolutiontext = self.font2.render('Resolution:', True, 'white')
        self.resolutiontextRect = self.resolutiontext.get_rect()
        self.resolutiontextRect.center = (
        self.width // 2 - self.width // 10, self.height // 2 - 2 * (self.height // 20 + self.height // 47))

        self.hoptext = self.font2.render('Hopbar location:', True, 'white')
        self.hoptextRect = self.hoptext.get_rect()
        self.hoptextRect.center = (
        self.width // 2 - self.width // 10, self.height // 2 - (self.height // 20 + self.height // 47))

        save_n_exit = button.ButtonForgame(71, self)

        self.DropdownMenus = []

        self.DropdownMenus = [dm.DropdownMenu(self, x) for x in range(3)]

        self.game.objects.append(self)


    def render(self):
        self.screen.blit(self.resolutiontext, self.resolutiontextRect)
        self.screen.blit(self.hoptext, self.hoptextRect)

        for object in self.objects:
            object.render()

    def checkevent(self, pos):
        for object in self.objects:
            object.checkcollision(pos)



