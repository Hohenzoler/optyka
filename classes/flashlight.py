import pygame
class Flashlight:  #creating a flash light class
    def __init__(self, x, y):
        self.width = 200
        self.heigh = 100
        self.x = x-self.width//2 #adjusted so that when someone creates a flashlight it places in the correct spot
        self.y = y-self.heigh//2
        self.rect = (self.x, self.y, self.width, self.heigh)
        self.transparent_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
        self.transparent_surface.fill((255, 255, 255, 50))  # last number is the alpha value (transparency)

    def draw(self, screen): # basic drawing functions
        pygame.draw.rect(screen, "grey", self.rect)

    def drawoutline(self, screen):
        screen.blit(self.transparent_surface, (self.x, self.y)) #draws a transparent outline of the flashlight at the mouse pos
