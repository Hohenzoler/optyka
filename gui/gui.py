import pygame
from classes import gameobjects, sounds

class GUI:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height // 10
        self.rect = pygame.Rect(0, height - self.height, self.width, self.height)
        self.Frect = pygame.Rect(10, height - self.height + 10, self.height - 20, self.height - 20)
        self.Fclicked = 0
        self.layer = 2  # Assign a higher layer value to GUI to ensure it's rendered on top
        self.objects1 = []
        self.game.objects.append(self)
        self.f=None

    def render(self):
        mousepos = pygame.mouse.get_pos()

        # flashlight
        if self.Fclicked == 1:
            if self.game.r:
                self.f.adjust(mousepos[0], mousepos[1], 1)
            else:
                self.f.adjust(mousepos[0], mousepos[1], 0)
            self.f.drawoutline()  # displaying a semi-transparent outline of the flashlight

        if self.Fclicked == 2:
            if self.game.r:
                self.f.adjust(mousepos[0], mousepos[1], 1)
            else:
                self.f.adjust(mousepos[0], mousepos[1], 0)
            self.game.objects.insert(-2, self.f)
            self.Fclicked = 0
            self.f = None
            sounds.placed_sound()

        # Check if the red button is clicked and change its color temporarily
        button_color = (255, 0, 0)  # Red color
        if self.Fclicked == 1:
            button_color = (150, 0, 0)  # Darken the color when clicked

        pygame.draw.rect(self.game.screen, (100, 100, 100), self.rect)
        pygame.draw.rect(self.game.screen, button_color, self.Frect)



    def checkifclicked(self, mousepos):
        if self.Frect.collidepoint(mousepos) and self.Fclicked == 0:
            self.Fclicked = 1
            self.f = gameobjects.Flashlight(self.game, mousepos[0], mousepos[1])
            sounds.selected_sound()
        elif self.Frect.collidepoint(mousepos) and self.Fclicked == 1:
            self.Fclicked = 0
        elif self.Frect.collidepoint(mousepos) is False and self.Fclicked == 1:
            self.Fclicked = 2
