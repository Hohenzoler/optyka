# gui.py
import pygame
from classes import sounds
from classes.gameobjects import Flashlight

class GUI:
    # Graphical User Interface class
    def __init__(self, game, width, height):
        # Initialize the GUI
        self.game = game
        self.width = width
        self.height = height // 10
        self.rect = pygame.Rect(0, height - self.height, self.width, self.height)
        self.Frect = pygame.Rect(10, height - self.height + 10, self.height - 20, self.height - 20)
        self.Fclicked = 0
        self.layer = 2
        self.objects1 = []
        self.game.objects.append(self)

    def render(self):
        # Render GUI elements
        mousepos = list(pygame.mouse.get_pos())
        mousepos[0] -= 100  # Centering the mouse
        mousepos[1] -= 50

        self.f = Flashlight(self.game, [(mousepos[0], mousepos[1]),
                                        (mousepos[0] + 200, mousepos[1]),
                                        (mousepos[0] + 200, mousepos[1] + 100),
                                        (mousepos[0], mousepos[1] + 100)], (255, 0, 0), 100, image_path="images/torch.png")

        def adjust_flashlight():
            self.f.adjust(self.f.points)

        if self.Fclicked == 1:
            if self.game.r:
                adjust_flashlight()
            else:
                adjust_flashlight()
            self.f.drawoutline()

        if self.Fclicked == 2:
            if self.game.r:
                adjust_flashlight()
            else:
                adjust_flashlight()

            self.f.light_adjust(self.f.points[0][0], self.f.points[0][1])
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
        # Check if GUI elements are clicked
        if self.Frect.collidepoint(mousepos) and self.Fclicked == 0:
            self.Fclicked = 1
            sounds.selected_sound()
        elif self.Frect.collidepoint(mousepos) and self.Fclicked == 1:
            self.Fclicked = 0
        elif not self.Frect.collidepoint(mousepos) and self.Fclicked == 1:
            self.Fclicked = 2
