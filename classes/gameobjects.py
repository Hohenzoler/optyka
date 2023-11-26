import random

import pygame
from classes import light, sounds
import math


class GameObject:

    def __init__(self, game, x, y, height, width, angle, color, islighting):
        self.game = game
        self.width = width
        self.height = height
        self.x = x - self.width // 2  # adjusted so that when someone creates a flashlight it places in the correct spot
        self.y = y - self.height // 2
        self.angle = angle
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(self.color)
        self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=self.rect.center)
        self.transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.transparent_surface.fill((255, 255, 255, 50))  # last number is the alpha value (transparency)
        self.on = True
        self.selectedtrue = False
        self.islighting = bool(islighting)  # it is boolean, true, false or maybe
        self.mousepos = None
        self.light = None
        self.light_width = 8
        self.layer = 1

    def render(self):
        if not self.selectedtrue:
            self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
            self.rotated_rect = self.rotated_surface.get_rect(center=self.rect.center)

            if self.islighting:
                if self.on:
                    # Calculate the starting point of the light from the center of the rotated rectangle/surface
                    rotated_center_x, rotated_center_y = self.rotated_rect.center

                    light_start_x = rotated_center_x
                    light_start_y = rotated_center_y

                    light_end_x = light_start_x + math.cos(math.radians(self.angle)) * 1000
                    light_end_y = light_start_y - math.sin(math.radians(self.angle)) * 1000

                    self.light = light.Light(self.game, ((light_start_x, light_start_y), (light_end_x, light_end_y)),
                                             "white", self.angle, self.light_width)
                elif not self.on:
                    self.light = None

            # Render the light before blitting the rotated surface
            light.Light.render(self.light)

            # Blit the rotated surface at the rotated_rect's topleft
            self.game.screen.blit(self.rotated_surface, self.rotated_rect.topleft)
        else:
            self.move()

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


class Flashlight(GameObject):  # Inheriting from GameObject
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 100, 200, random.randint(1, 355), "red", True)  # Call the constructor of the parent class

