import pygame
from classes import flashlight


class GUI:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height // 10
        self.rect = pygame.Rect(0, height - self.height, self.width, self.height)
        self.Frect = pygame.Rect(10, height - self.height + 10, self.height - 20, self.height - 20)  # rect for the button to create a flashlight
        self.Fclicked = 0  # a bullion that tells whether the flashlight button has been clicked or not
        self.objects1 = []
        self.game.objects.append(self)

    def render(self):
        mousepos = pygame.mouse.get_pos()
        f = flashlight.Flashlight(self.game, mousepos[0], mousepos[1])  # flashlight
        if self.Fclicked == 1:
            f.drawoutline()  # displaying a semi-transparent outline of the flashlight
        if self.Fclicked == 2:
            self.game.objects.insert(-2, f)
            self.Fclicked = 0

        pygame.draw.rect(self.game.screen, (100, 100, 100), self.rect)
        pygame.draw.rect(self.game.screen, 'red', self.Frect)

    def checkifclicked(self, mousepos):
        if self.Frect.collidepoint(mousepos) and self.Fclicked == 0:
            self.Fclicked = 1
        elif self.Frect.collidepoint(mousepos) and self.Fclicked == 1:
            self.Fclicked = 0
        elif self.Frect.collidepoint(mousepos) == False and self.Fclicked == 1:
            self.Fclicked = 2
