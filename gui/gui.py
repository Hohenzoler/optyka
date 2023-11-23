import pygame
from classes import flashlight

class GUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height//10
        self.rect = pygame.Rect(0, height - self.height, self.width, self.height)
        self.Frect = pygame.Rect(10, height - self.height + 10, self.height-20, self.height-20) #rect for the button to create a flashlight
        self.Fclicked = 0 #a bullion that tells whether the flashlight button has been clicked or not

    def draw(self, screen):
        mousepos = pygame.mouse.get_pos()
        f = flashlight.Flashlight(mousepos[0], mousepos[1]) #flashlight
        if self.Fclicked:
            f.drawoutline(screen) #displaying a semi-transparent outline of the flashlight
        if self.Fclicked == 2:
            from main import objects
            self.Fclicked = 0
            objects.insert(-1, f) #appending the flashlight in the secound to last position so that the gui is on top

        pygame.draw.rect(screen, "grey", self.rect)
        pygame.draw.rect(screen, 'red', self.Frect)
        print(self.Fclicked)

    def checkifclicked(self, mousepos):
        if self.Frect.collidepoint(mousepos) and self.Fclicked == False:
            self.Fclicked = 1
        elif self.Frect.collidepoint(mousepos) and self.Fclicked == True:
            self.Fclicked = 0
        elif self.Fclicked == True:
            self.Fclicked = 2


