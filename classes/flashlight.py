import pygame
from classes import light


class Flashlight:  # creating a flash light class
    def __init__(self, game, x, y):
        self.game = game
        self.width = 200
        self.heigh = 100
        self.x = x - self.width // 2  # adjusted so that when someone creates a flashlight it places in the correct spot
        self.y = y - self.heigh // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.heigh)
        self.transparent_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
        self.transparent_surface.fill((255, 255, 255, 50))  # last number is the alpha value (transparency)
        self.on = True
        self.selectedtrue = False

    def render(self):  # basic drawing functions
        mousepos = pygame.mouse.get_pos()
        if not self.selectedtrue:
            pygame.draw.rect(self.game.screen, "grey", self.rect)
            if self.on:
                self.light = light.Light(self.game, ([self.x + self.width, self.y + self.heigh // 2], [self.game.width, self.y + self.heigh // 2]),(255, 255, 255))
            elif not self.on:
                self.light = None

        else:
            self.x = mousepos[0] - self.width//2
            self.y = mousepos[1] - self.heigh//2
            self.rect = pygame.Rect(self.x, self.y, self.width, self.heigh)
            self.game.screen.blit(self.transparent_surface, (self.x, self.y))

    def drawoutline(self):
        self.game.screen.blit(self.transparent_surface, (self.x, self.y))  # draws a transparent outline of the flashlight at the mouse pos.

    def checkifclicked(self, mousepos):
        if self.rect.collidepoint(mousepos):
            if self.on == 1:
                self.on = 0
            else:
                self.on = 1

    def selected(self, mousepos):
        if self.rect.collidepoint(mousepos) and self.selectedtrue == False:
            self.selectedtrue = True

        elif self.rect.collidepoint(mousepos) and self.selectedtrue == True:
            self.selectedtrue = False

