import pygame
from classes import gameobjects, sounds

class Button:
    def __init__(self, game, number, y):
        self.game = game
        self.number = number
        self.screenheight = self.game.height
        self.y = y
        self.rect = pygame.Rect(60*self.number + 10, self.screenheight - self.y + 10, self.y - 20, self.y - 20)

        if self.number == 0:
            self.color = (255, 0, 0)
        elif self.number == 1:
            self.color = (0, 0, 255)
        elif self.number == 2:
            self.color = (0, 255, 0)
        else:
            self.color = (255, 255, 255)

        self.clicked = 0 #0 means the button is not clicked, 1 means the button was clicked and is currently active and 2 means that the selectd object is being placed and the button will revert to 0 afterwards.

    def render(self):
        mousepos = pygame.mouse.get_pos()
        # flashlight
        if self.number == 0:
            if self.clicked == 1:
                if self.game.r:
                    self.f.adjust(mousepos[0], mousepos[1], 1)
                else:
                    self.f.adjust(mousepos[0], mousepos[1], 0)
                self.f.drawoutline()  # displaying a semi-transparent outline of the flashlight

            if self.clicked == 2:
                if self.game.r:
                    self.f.adjust(mousepos[0], mousepos[1], 1)
                else:
                    self.f.adjust(mousepos[0], mousepos[1], 0)
                self.f.light_adjust()
                self.game.objects.insert(-2, self.f)
                self.clicked = 0
                self.f = None
                sounds.placed_sound()

        elif self.number == 1:
            if self.clicked == 1:
                print('Hello Terraria User')
            if self.clicked == 2:
                self.clicked = 0




        pygame.draw.rect(self.game.screen, self.color, self.rect)

    def checkifclicked(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            mousepos = pygame.mouse.get_pos()
            if self.clicked == 0:
                self.clicked = 1
                if self.number == 0:
                    self.f = gameobjects.Flashlight(self.game, mousepos[0], mousepos[1])
                sounds.selected_sound()
            elif self.rect.collidepoint(mousepos) and self.clicked == 1:
                self.clicked = 0
                sounds.selected_sound()
        elif self.rect.collidepoint(pos) is False and self.clicked == 1:
            self.clicked = 2



