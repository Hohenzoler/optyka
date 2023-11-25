import pygame
from classes import light


class GameObject:

    def __init__(self, game, x, y, height, width, angle, color, islighting):
        self.game = game
        self.width = width
        self.height = height
        self.x = x - self.width // 2  # adjusted so that when someone creates a flashlight it places in the correct spot
        self.y = y - self.height // 2
        self.angle = angle
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.transparent_surface.fill((255, 255, 255, 50))  # last number is the alpha value (transparency)
        self.on = True
        self.selectedtrue = False
        self.islighting = bool(islighting) # it is boolean, true, false or maybe

    def render(self):
        if not self.selectedtrue:
            pygame.draw.rect(self.game.screen, self.color, self.rect)
            if self.islighting: #checks atridbute isLighting
                if self.on: #checks atribute on, which probably checks is object is clicked
                    self.light = light.Light(self.game, (
                        [self.x + self.width, self.y + self.height // 2], [self.game.width, self.y + self.height // 2]),
                                             "white")
                elif not self.on:
                    self.light = None
        else:
            self.move()


    def move(self): #code for movimg object with mouse
        self.mousepos = pygame.mouse.get_pos()
        self.x = self.mousepos[0] - self.width // 2
        self.y = self.mousepos[1] - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.game.screen.blit(self.transparent_surface, (self.x, self.y))

    def drawoutline(self):
        rotated_surface = pygame.transform.rotate(self.transparent_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        self.game.screen.blit(rotated_surface, rotated_rect.topleft) # draws a transparent outline of the flashlight at the mouse pos

    def checkifclicked(self, mousepos): #checks if object is clicked
        if self.rect.collidepoint(mousepos):
            if self.on == 1:
                self.on = 0
            else:
                self.on = 1

    def selected(self, mousepos): #checks if object is selected
        if self.rect.collidepoint(mousepos) and self.selectedtrue is False:
            self.selectedtrue = True

        elif self.rect.collidepoint(mousepos) and self.selectedtrue is True:
            self.selectedtrue = False


class Flashlight(GameObject):  # Inheriting from GameObject
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 100, 200, 20, "blue", True)  # Call the constructor of the parent class

