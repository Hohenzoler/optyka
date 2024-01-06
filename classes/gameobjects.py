import pygame
from classes import light, sounds
import math
from pygame.transform import rotate

class GameObject:

    def __init__(self, game, points, color, angle, image_path=None):
        # Initialize common attributes
        self.game = game
        self.points = points
        self.color = color
        self.on = True
        self.selectedtrue = False
        self.mousepos = None
        self.layer = 1
        self.placed = False
        self.angle = angle
        self.image_path = image_path
        self.image = pygame.image.load(image_path) if image_path else None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect()

    def update_rect(self):
        # Update the rect based on the points
        min_x = min(pt[0] for pt in self.points)
        min_y = min(pt[1] for pt in self.points)
        max_x = max(pt[0] for pt in self.points)
        max_y = max(pt[1] for pt in self.points)
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def render(self):
        if not self.selectedtrue:
            # Rotate the points of the object
            rotated_points = self.rotate_points(self.points, self.angle)

            # Render the image if available
            if self.image:
                center_x = sum(x for x, _ in rotated_points) / len(rotated_points)
                center_y = sum(y for _, y in rotated_points) / len(rotated_points)
                rotated_image = rotate(self.image, -self.angle)
                image_rect = rotated_image.get_rect(center=(center_x, center_y))

                # Blit the rotated image without transparency
                self.game.screen.blit(rotated_image, image_rect.topleft)
            else:
                # Draw the rotated lines without transparency
                pygame.draw.polygon(self.game.screen, self.color, rotated_points)
        else:
            mousepos = pygame.mouse.get_pos()
            if self.game.r:
                self.adjust(mousepos[0], mousepos[1], 1)
            else:
                self.adjust(mousepos[0], mousepos[1], 0)
            self.drawoutline()

    def rotate_points(self, points, angle):
        # Rotate points around the center of the object
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

    def adjust(self, x, y, d_angle):
        # Adjust the object's position and angle
        self.angle += d_angle
        self.x = x - sum(pt[0] for pt in self.points) / len(self.points)
        self.y = y - sum(pt[1] for pt in self.points) / len(self.points)

        # Update the points based on the new position and angle
        self.points = self.rotate_points(self.points, d_angle)

        # Assuming self.transparent_surface is a surface with transparency
        # Blit the rotated image with transparency
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, -self.angle)
            image_rect = rotated_image.get_rect(center=((self.x + sum(pt[0] for pt in self.points) / len(self.points)),
                                                        (self.y + sum(pt[1] for pt in self.points) / len(self.points))))
            self.game.screen.blit(rotated_image, image_rect.topleft)
            # Draw the rotated lines without transparency
            #rotated_points = self.rotate_points(self.points, self.angle)
            self.points = [(x + self.x, y + self.y) for x, y in self.points]
            self.update_rect()

        else:
            self.points = [(x + self.x, y + self.y) for x, y in self.points]
            pygame.draw.polygon(self.game.screen, self.color, self.points)
            self.update_rect()

    def move(self):
        # code for moving object with mouse
        self.mousepos = pygame.mouse.get_pos()

        # Calculate the average position of the object's vertices
        center_x = sum(x for x, _ in self.points) / len(self.points)
        center_y = sum(y for _, y in self.points) / len(self.points)

        # Update the position based on the mouse cursor
        self.x = self.mousepos[0] - center_x
        self.y = self.mousepos[1] - center_y

        # Assuming self.transparent_surface is a surface with transparency
        # Blit the rotated image with transparency
        if self.image:
            rotated_image = rotate(self.image, -self.angle)
            image_rect = rotated_image.get_rect(center=(self.x + center_x, self.y + center_y))
            self.game.screen.blit(rotated_image, image_rect.topleft)
            # Draw the rotated lines without transparency
            rotated_points = self.rotate_points(self.points, self.angle)
            self.points = [(x + self.x, y + self.y) for x, y in rotated_points]
            self.update_rect()
        else:
            pygame.draw.polygon(self.game.screen, self.color, self.points)
    def drawoutline(self):
        # Draw an outline around the object
        pygame.draw.lines(self.game.screen, (255, 255, 255), True, self.points, 2)

    def checkifclicked(self, mousepos):
        # Check if the object is clicked
        mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        pygame.draw.polygon(mask_surface, (255, 255, 255, 1), self.points)

        if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0:
            if self.on == 1:
                self.on = 0
            else:
                self.on = 1

    def selected(self, mousepos):
        # Check if the object is selected
        mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        pygame.draw.polygon(mask_surface, (255, 255, 255, 1), self.points)

        if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0 and not self.selectedtrue:
            self.selectedtrue = True
            sounds.selected_sound()
        elif mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0 and self.selectedtrue:
            self.selectedtrue = False
            if type(self) == Flashlight:
                sounds.laser_sound()
            else:
                sounds.placed_sound()

class Mirror(GameObject):
    def __init__(self, game, points, color, angle, islighting=False, image_path=None):
        super().__init__(game, points, color, angle, image_path)


class Flashlight(GameObject):  # Inheriting from GameObject
    def __init__(self, game, points, color, angle, islighting=True, image_path=None):
        super().__init__(game, points, color, angle, image_path)
        self.islighting = bool(islighting)
        self.light = None
        self.light_width = 8
        self.color = color
        self.angle = angle
        self.image_path = image_path
        self.image = pygame.image.load(image_path) if image_path else None

    def render(self):
        super().render()
        if self.islighting:
            if self.on:
                # Calculate the starting point of the light from the center of the rotated rectangle/surface
                center_x = sum(x for x, _ in self.points) / len(self.points)
                center_y = sum(y for _, y in self.points) / len(self.points)

                self.light_adjust(center_x, center_y)

                self.light = light.Light(self.game,
                                         [[self.light_start_x, self.light_start_y]],
                                         "white", -1*self.angle, self.light_width)
                self.light.trace_path()
                self.placed = True
                # self.light = light.Light(self.game, ((self.light_start_x, self.light_start_y), (self.light_end_x, self.light_end_y)),"white", self.angle, self.light_width)

                # Render the light before blitting the rotated surface
                light.Light.render(self.light)
                self.game.objects.remove(self.light)
            elif not self.on:
                self.light = None

            super().render()

    def light_adjust(self, center_x, center_y):
        self.light_start_x = center_x
        self.light_start_y = center_y
        # Adjust the flashlight light position and direction
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
            # self.angle = math.degrees(math.atan2(normalized_direction[1], normalized_direction[0]))
