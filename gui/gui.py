import pygame
from classes import flashlight

class GUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height//10
        self.rect = pygame.Rect(0, height - self.height, self.width, self.height)
        self.Frect = pygame.Rect(10, height - self.height + 10, self.height-20, self.height-20) #rect for the button to create a flashlight
        self.Fclicked = 0 #a bullion that tells whether the flashlight button has been clicked or not
        self.objects1 = []

    def draw(self, screen):
        mousepos = pygame.mouse.get_pos()
        f = flashlight.Flashlight(mousepos[0], mousepos[1]) #flashlight
        if self.Fclicked == 1:
            f.drawoutline(screen) #displaying a semi-transparent outline of the flashlight
        if self.Fclicked == 2:
            self.objects1.append(f) #appending the flashlight to an internal list so it can later be transfered to the objects list to be drawn
            self.Fclicked = 0

        pygame.draw.rect(screen, "grey", self.rect)
        pygame.draw.rect(screen, 'red', self.Frect)

    def checkifclicked(self, mousepos):
        if self.Frect.collidepoint(mousepos) and self.Fclicked == 0:
            self.Fclicked = 1
        elif self.Frect.collidepoint(mousepos) and self.Fclicked == 1:
            self.Fclicked = 0
        elif self.Frect.collidepoint(mousepos) == False and self.Fclicked == 1:
            self.Fclicked = 2