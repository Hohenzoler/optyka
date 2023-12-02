import pygame
from classes import light, sounds
import math

class GameObject:
    def __init__(self, game, points, color):
        self.game = game
        self.points = points
        self.color = color
        self.on = True
        self.selectedtrue = False
        self.mousepos = None
        self.layer = 1
        self.placed = False

    def render(self):
        if not self.selectedtrue:
            pygame.draw.lines(self.game.screen, self.color, True, self.points, 2)
        else:
            self.move()

    def adjust(self, points):
        self.points = points

    def move(self):
        self.mousepos = pygame.mouse.get_pos()
        self.adjust([(x + self.mousepos[0], y + self.mousepos[1]) for x, y in self.points])

    def drawoutline(self):
        pygame.draw.lines(self.game.screen, (255, 255, 255), True, self.points, 2)

    def checkifclicked(self, mousepos):
        mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        pygame.draw.polygon(mask_surface, (255, 255, 255, 0), self.points)

        if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0:
            if self.on == 1:
                self.on = 0
            else:
                self.on = 1

    def selected(self, mousepos):
        mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        pygame.draw.polygon(mask_surface, (255, 255, 255, 0), self.points)

        if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0 and not self.selectedtrue:
            self.selectedtrue = True
            sounds.selected_sound()
        elif mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0 and self.selectedtrue:
            self.selectedtrue = False
            sounds.placed_sound()

class Flashlight(GameObject):  # Inheriting from GameObject
    def __init__(self, game, points, islighting=True):
        super().__init__(game, points, (255, 255, 255))  # Call the constructor of the parent class
        self.islighting = bool(islighting)  # it is boolean, true, false or maybe
        self.light = None
        self.light_width = 8
        self.angle = 100 # Add the angle attribute and initialize it

    def render(self):
        super().render()

        if self.islighting:
            if not self.placed:
                if self.on:
                    # Calculate the starting point of the light from the center of the rotated rectangle/surface
                    center_x = sum(x for x, _ in self.points) / len(self.points)
                    center_y = sum(y for _, y in self.points) / len(self.points)

                    self.light_adjust(center_x, center_y)

                    self.light = light.Light(self.game, self.points, "white", self.angle, self.light_width)
                    self.placed = True

                    # Render the light before blitting the rotated surface
                    light.Light.render(self.light)
            elif not self.on:
                self.light = None

    def light_adjust(self, center_x, center_y):
        self.light_start_x = center_x
        self.light_start_y = center_y

        angle = math.degrees(math.atan2(self.points[0][1] - center_y, self.points[0][0] - center_x))
        self.light_end_x = center_x + math.cos(math.radians(angle)) * 1000
        self.light_end_y = center_y + math.sin(math.radians(angle)) * 1000

