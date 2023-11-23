import pygame
class Flashlight:  #creating a flash light class
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.heigh = 100
        self.rect = (self.x, self.y, self.width, self.heigh)

    def draw(self, screen): # basic drawing functions
        pygame.draw.rect(screen, "grey", self.rect)