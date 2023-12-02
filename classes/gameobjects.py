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
            # Rotate the points of the object
            rotated_points = self.rotate_points(self.points, self.angle)

            # Draw the rotated lines
            pygame.draw.lines(self.game.screen, self.color, True, rotated_points, 2)
        else:
            self.move()

    def rotate_points(self, points, angle):
        # Calculate the center of the object
        center_x = sum(x for x, _ in points) / len(points)
        center_y = sum(y for _, y in points) / len(points)

        # Create a new list to store the rotated points
        rotated_points = []

        # Rotate each point around the center
        for x, y in points:
            # Translate the point to the origin
            translated_x = x - center_x
            translated_y = y - center_y

            # Rotate the translated point
            rotated_x = translated_x * math.cos(math.radians(angle)) - translated_y * math.sin(math.radians(angle))
            rotated_y = translated_x * math.sin(math.radians(angle)) + translated_y * math.cos(math.radians(angle))

            # Translate the rotated point back to the original position
            final_x = rotated_x + center_x
            final_y = rotated_y + center_y

            # Add the rotated point to the list
            rotated_points.append((final_x, final_y))

        return rotated_points

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

                    self.light = light.Light(self.game, [(center_x, center_y),
                                                         (self.light_end_x, self.light_end_y)], "white", self.angle,
                                             self.light_width)
                    self.placed = True

                    # Render the light before blitting the rotated surface
                    light.Light.render(self.light)
            elif not self.on:
                self.light = None

    def light_adjust(self, center_x, center_y):
        # Calculate the direction vector from the center to one of the points
        direction_vector = (self.points[0][0] - center_x, self.points[0][1] - center_y)

        # Calculate the length of the direction vector
        length = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)

        # Check if the length is not zero before normalizing
        if length != 0:
            # Normalize the direction vector
            normalized_direction = (direction_vector[0] / length, direction_vector[1] / length)

            # Calculate the end point of the light
            self.light_end_x = center_x + normalized_direction[0] * 1000
            self.light_end_y = center_y + normalized_direction[1] * 1000

            # Calculate the angle between the normalized direction and the x-axis
            self.angle = math.degrees(math.atan2(normalized_direction[1], normalized_direction[0]))



