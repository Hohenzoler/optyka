import random

import pygame
from classes import light, sounds
import math


class GameObject:

    def __init__(self, game, x, y, height, width, angle, color, image_path):
        self.game = game
        self.width = width
        self.height = height
        self.x = x - self.width // 2  # adjusted so that when someone creates a flashlight it places in the correct spot
        self.y = y - self.height // 2
        self.angle = angle
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.on = True
        self.selectedtrue = False
        self.mousepos = None
        self.layer = 1
        self.placed = False
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        self.transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.transparent_surface.blit(self.image, (0, 0))
        self.transparent_surface.set_alpha(100)

    def render(self):
        if not self.selectedtrue:
            # Rotate the surface around its center
            self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
            self.rotated_rect = self.rotated_surface.get_rect(center=self.rect.center)

            # Blit the rotated surface at the rotated_rect's topleft
            self.game.screen.blit(self.rotated_surface, self.rotated_rect.topleft)
        else:
            mousepos = pygame.mouse.get_pos()
            if self.game.r:
                self.adjust(mousepos[0], mousepos[1], 1)
            else:
                self.adjust(mousepos[0], mousepos[1], 0)
            self.drawoutline()

    def adjust(self, x, y, d_angle):
        self.angle += d_angle
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=self.rect.center)
        self.rotated_center_x, self.rotated_center_y = self.rotated_rect.center

    def move(self):  # code for movimg object with mouse
        self.mousepos = pygame.mouse.get_pos()
        self.x = self.mousepos[0] - self.width // 2
        self.y = self.mousepos[1] - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.game.screen.blit(self.transparent_surface, (self.x, self.y))

    def drawoutline(self):
        rotated_surface = pygame.transform.rotate(self.transparent_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        self.game.screen.blit(rotated_surface,
                              rotated_rect.topleft)  # draws a transparent outline of the flashlight at the mouse pos

    def checkifclicked(self, mousepos):  # checks if object is clicked
        if self.rect.collidepoint(mousepos):
            if self.on == 1:
                self.on = 0
            else:
                self.on = 1

    def selected(self, mousepos):  # checks if object is selected
        if self.rect.collidepoint(mousepos) and self.selectedtrue is False:
            self.selectedtrue = True
            sounds.selected_sound()

        elif self.rect.collidepoint(mousepos) and self.selectedtrue is True:
            self.selectedtrue = False
            sounds.placed_sound()
class Mirror(GameObject):
    def __init__(self, game, x, y, height, width, angle, color, image_path):
        super().__init__( game, x, y, height, width, angle, color, image_path)  # Call the constructor of the parent class

class Flashlight(Mirror):  # Inheriting from GameObject
    def __init__(self, game, x, y, islighting=True):
        super().__init__(game, x, y, 100, 200, 0, "red", "images/torch.png")  # Call the constructor of the parent class
        self.islighting = bool(islighting)  # it is boolean, true, false or maybe
        self.light = None
        self.light_width = 8

    def render(self):
        super().render()

        if self.islighting:
            if self.on:
                # Calculate the starting point of the light from the center of the rotated rectangle/surface
                self.rotated_center_x, self.rotated_center_y = self.rotated_rect.center

                self.light_adjust()

                self.light = light.Light(self.game,
                                             [[self.light_start_x, self.light_start_y]],
                                             "white", self.angle, self.light_width)
                self.light.trace_path()
                self.placed = True
                # self.light = light.Light(self.game, ((self.light_start_x, self.light_start_y), (self.light_end_x, self.light_end_y)),"white", self.angle, self.light_width)

                # Render the light before blitting the rotated surface
                light.Light.render(self.light)
                self.game.objects.remove(self.light)
            elif not self.on:
                self.light = None

            super().render()

    def light_adjust(self):
        self.light_start_x = self.rotated_center_x
        self.light_start_y = self.rotated_center_y

        self.light_end_x = self.light_start_x + math.cos(math.radians(self.angle)) * 1000
        self.light_end_y = self.light_start_y - math.sin(math.radians(self.angle)) * 1000



