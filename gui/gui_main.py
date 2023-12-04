import pygame
from gui import button


class GUI:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height // 10
        self.rect = pygame.Rect(0, height - self.height, self.width, self.height)
        self.layer = 2  # Assign a higher layer value to GUI to ensure it's rendered on top
        self.game.objects.append(self)
        self.f = None

        self.buttons = [button.Button(self.game, x, self.height) for x in range(3)] #creates buttons


    def render(self):
        pygame.draw.rect(self.game.screen, (100, 100, 100), self.rect)
        for button in self.buttons: #renders buttons
            button.render()

    def checkifclicked(self, mousepos):
        for button in self.buttons:
            button.checkifclicked(mousepos)