import pygame
class GUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height//10
        self.rect = pygame.Rect(0, height - self.height, self.width, self.height)
        self.Frect = pygame.Rect(10, height - self.height + 10, self.height-20, self.height-20) #rect for the button to create a flashlight

    def draw(self, screen):
        pygame.draw.rect(screen, "grey", self.rect)
        pygame.draw.rect(screen, 'red', self.Frect)

    def checkifclicked(self, mousepos):
        if self.Frect.collidepoint(mousepos):
            print('a')
