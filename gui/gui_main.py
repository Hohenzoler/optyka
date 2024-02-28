import pygame
from gui import button
from classes import bin

class GUI:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height // 10
        self.position = self.game.settings['HOTBAR_POSITION']

        if self.position == 'bottom':
            self.rect = pygame.Rect(0, self.height*10 - self.height, self.width, self.height)
        elif self.position == 'left':
            self.rect = pygame.Rect(0, 0, self.width//10, self.height*10)
            # self.game.achievements.handle_achievement_unlocked("U are weird...")
        elif self.position == 'right':
            self.rect = pygame.Rect(self.width - self.width//10, 0, self.width//10, self.height*10)
            # self.game.achievements.handle_achievement_unlocked("U are weird...")
        elif self.position == 'top':
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            # self.game.achievements.handle_achievement_unlocked("U are weird...")


        self.layer = 3  # Assign a higher layer value to GUI to ensure it's rendered on top
        self.game.objects.append(self)
        self.f = None


        self.bin = bin.Bin(self.game)

        self.button_min = -3
        self.button_max = 7

        self.buttons = [button.Button(self.game, x, tooltip_text=self.tooltip_list(x)) for x in
                        range(self.button_min, self.button_max)]  # creates buttons


    def render(self):
        pygame.draw.rect(self.game.screen, (100, 100, 100), self.rect)
        for button in self.buttons: #renders buttons
            button.render()

    def checkifclicked(self, mousepos):
        if self.game.selected_object is not None:
            return
        for button in self.buttons:
            button.checkifclicked(mousepos)


    def tooltip_list(self, id):
        if id == -3:
            return "Achievements"
        elif id == -2:
            return "Settings"
        elif id == -1:
            return "Quit"
        elif id == 0:
            return "Flashlight"
        elif id == 1:
            return "Mirror"
        elif id == 2:
            return "Colored Glass"
        elif id == 3:
            return "Prism"
        elif id == 4:
            return "Drawing Mode"
        elif id == 5:
            return "Lens"
        elif id == 6:
            return "Corridor"
        else:
            return "Unknown"

    def load_settings(self):
        self.width = self.game.width
        self.height = self.game.height // 10
        self.position = self.game.settings['HOTBAR_POSITION']

        if self.position == 'bottom':
            self.rect = pygame.Rect(0, self.height * 10 - self.height, self.width, self.height)
        elif self.position == 'left':
            self.rect = pygame.Rect(0, 0, self.width // 10, self.height * 10)
        elif self.position == 'right':
            self.rect = pygame.Rect(self.width - self.width // 10, 0, self.width // 10, self.height * 10)
        elif self.position == 'top':
            self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.buttons = [button.Button(self.game, x, tooltip_text=self.tooltip_list(x)) for x in range(self.button_min, self.button_max)] #creates buttons