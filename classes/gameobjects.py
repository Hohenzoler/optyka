import time
import functions
import pygame
from gui import ModifyParameters as mp
from classes import light, sounds, images
import math
from pygame.transform import rotate
import random
import settingsSetup
from pygame import gfxdraw
from classes import bin
from gui.gui_main import GUI
settings = settingsSetup.start()

NUM_RAYS = settings['Flashlight_Rays']
FOV = settings['Flashlight_FOV']
HALF_FOV = FOV / 2
DELTA_ANGLE = FOV / NUM_RAYS

class GameObject:

    def __init__(self, game, points, color, angle, reflection_factor, image = None, texture =None, textureName=None):
        # Initialize common attributes
        self.game = game
        self.points = points

        self.texture = texture if texture else None
        self.textureName = textureName if self.texture else None

        self.color = color if not self.texture else None

        self.on = True
        self.selectedtrue = False
        self.mousepos = None
        self.layer = 1
        self.placed = False
        self.angle = angle
        self.image = image if image else None

        self.reflection_factor = reflection_factor

        if image != None:
            self.image_width = self.image.get_width()
            self.image_height = self.image.get_height()

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.triangles_generated = False
        self.update_rect()

        self.scale_factor = 1
        self.lazer = False
        self.parameters_counters = 0

        self.find_parameters()

    def update_rect(self):
        # Update the rect based on the points
        min_x = min(pt[0] for pt in self.points)
        min_y = min(pt[1] for pt in self.points)
        max_x = max(pt[0] for pt in self.points)
        max_y = max(pt[1] for pt in self.points)
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    def get_triangles(self):
        # Check if triangles have already been generated
        if not self.triangles_generated:
            center_x = sum(x for x, _ in self.points) / len(self.points)
            center_y = sum(y for _, y in self.points) / len(self.points)
            self.triangles = [((center_x, center_y), (self.points[i][0], self.points[i][1]),(self.points[i + 1][0], self.points[i + 1][1])) for i in range(len(self.points) - 1)]
            self.triangles.append(((center_x, center_y), (self.points[len(self.points) - 1][0],self.points[len(self.points) - 1][1]),(self.points[0][0], self.points[0][1])))
            self.triangles_generated = True  # Set the flag to True after generating triangles

        return self.triangles
    def get_slopes(self):
        self.slopes=[(self.points[i],self.points[i+1]) for i in range(len(self.points)-1)]
        self.slopes.append((self.points[len(self.points)-1],self.points[0]))



    def draw_triangle(self,index):
        pygame.gfxdraw.aapolygon(self.game.screen, (255, 255, 255), self.triangles[index])
    def render(self):
        # print(self.get_triangles())

        self.get_slopes()


        if not self.selectedtrue:

            # Render the image if available
            if self.image:
                center_x = sum(x for x, _ in self.points) / len(self.points)
                center_y = sum(y for _, y in self.points) / len(self.points)

                self.image = pygame.transform.scale(self.image, (self.image_width*self.scale_factor, self.image_height*self.scale_factor))

                rotated_image = rotate(self.image, -self.angle)
                image_rect = rotated_image.get_rect(center=(center_x, center_y))

                image_rect = pygame.Rect(image_rect[0], image_rect[1], image_rect[2]*self.scale_factor, image_rect[3]*self.scale_factor)

                # Blit the rotated image without transparency
                self.game.screen.blit(rotated_image, image_rect.topleft)
            else:
                # Draw the rotated lines without transparency
                if self.texture:
                    pygame.gfxdraw.textured_polygon(self.game.screen, self.points, self.texture, int(self.x), int(self.y))
                else:
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)

        else:
            mousepos = pygame.mouse.get_pos()
            if self.game.r:

                self.adjust(mousepos[0], mousepos[1], self.game.r)
                self.game.r = False

            elif self.game.p:
                self.change_parameters()
                self.selectedtrue = False

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
        self.angle += d_angle
        self.x = x - sum(pt[0] for pt in self.points) / len(self.points)
        self.y = y - sum(pt[1] for pt in self.points) / len(self.points)

        temp_rect = self.rect.move(self.x, self.y)

        pygame.gfxdraw.rectangle(self.game.screen, temp_rect, (255, 255, 255))

        for obj in self.game.objects:
            if obj.rect.colliderect(temp_rect):
                if obj != self and isinstance(obj, GameObject):
                    return

        # Reset the flag to regenerate triangles
        self.triangles_generated = False

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
            mousepos = pygame.mouse.get_pos()
            if self.texture:
                pygame.gfxdraw.textured_polygon(self.game.screen, self.points, self.texture, mousepos[0], -mousepos[1])
            else:
                pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)
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

            mousepos = pygame.mouse.get_pos()
            if self.texture:
                pygame.gfxdraw.textured_polygon(self.game.screen, self.points, self.texture, mousepos[0], -mousepos[1])
            else:
                pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)
    def drawoutline(self):
        # Draw an outline around the object
        pygame.gfxdraw.aapolygon(self.game.screen, self.points, (255, 255, 255))
        if settings['DEBUG'] == "True":
            pygame.draw.rect(self.game.screen, (255, 255, 0), self.rect, 2) # draw object hitbox

    def checkifclicked(self, mousepos):
        # Check if the object is clicked
        mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        pygame.gfxdraw.filled_polygon(mask_surface, self.points, (255, 255, 255))

        if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0:
            if self.on == 1:
                self.on = 0
            else:
                self.on = 1

    def selected(self, mousepos):
        mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        pygame.gfxdraw.filled_polygon(mask_surface, self.points, (255, 255, 255))

        if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0:
            if self.game.selected_object is not None and self.game.selected_object != self:
                self.game.selected_object.selectedtrue = False  # Deselect the currently selected object

            if not self.selectedtrue:
                self.selectedtrue = True
                self.game.selected_object = self  # Set this object as the currently selected object
                sounds.selected_sound()
            else:
                self.selectedtrue = False
                self.game.selected_object = None  # No object is selected now
                if type(self) == Flashlight:
                    sounds.laser_sound()
                else:
                    sounds.placed_sound()

    def find_parameters(self):
        centerx = sum(x[0] for x in self.points) / len(self.points)
        centery = sum(y[1] for y in self.points) / len(self.points)

        self.parameters = {'x':centerx, 'y':centery, 'angle':self.angle}

        self.parameters['size'] = self.scale_factor

        self.parameters['reflection_factor'] = self.reflection_factor

        if type(self) == Flashlight:
            lazer_on = {'lazer': self.lazer}
            self.parameters.update(lazer_on)

        if self.color != None:
            colors = {'red': self.color[0], 'green': self.color[1], 'blue': self.color[2]}
            self.parameters.update(colors)


    def change_parameters(self, placeholder=None):
        if placeholder == None:
            self.find_parameters()
            mp.Parameters(self)

        try:
            d_angle = self.parameters['angle'] - self.angle
            self.adjust(self.parameters['x'], self.parameters['y'], d_angle)
            self.scale_factor = self.parameters['size']
            self.color = (self.parameters['red'], self.parameters['green'], self.parameters['blue'])
            self.lazer = self.parameters["lazer"]

        except Exception as e:
            print(e)


class Mirror(GameObject):
    def __init__(self, game, points, color, angle, reflection_factor, islighting=False, image_path=None, texture = None, textureName=None):
        super().__init__(game, points, color, angle, reflection_factor, image_path, texture, textureName)

class Prism(GameObject):
    def __init__(self, game, points, color, angle, reflection_factor, islighting=False, image_path=None, texture = None):
        super().__init__(game, points, color, angle, reflection_factor, image_path, texture)

class ColoredGlass(GameObject):
    def __init__(self, game, points, color, angle, reflection_factor, islighting=False, image_path=None, texture = None):
        super().__init__(game, points, color, angle, reflection_factor, image_path, texture)

class Lens(GameObject):
    def __init__(self, game, points, color, angle, type, curvature_radius, reflection_factor, islighting=False, image_path=None):
        super().__init__(game, points, color, angle, reflection_factor, image_path)
        self.curvature_radius = curvature_radius
        self.type = type
        self.CONVEX = 0
        self.CONCAVE = 1


    # def calculate_function(self, x1, x2, ymin):
    #     c = ymin
    #     a = c / (x1*x2)
    #     b = (x1 + x2)*(-a)
    #     print(f'{a}x2 + {b}x + {c}')
    #     return a, b, c

    # def generate_points_old(self, rect_points, angle):
    #     rect_points = self.rotate_points(rect_points, -90)
    #     x1 = rect_points[0][0]
    #     x2 = rect_points[2][0]
    #     x_offset = min(x1, x2) + abs(x1 - x2)/2#
    #     y_offset = min(rect_points[0][1], rect_points[2][1]) + abs(rect_points[0][1] - rect_points[2][1])#
    #     width = abs(x1 - x2)
    #     height = abs(rect_points[0][1] - rect_points[2][1])
    #     x1 = -width/2
    #     x2 = width/2
    #     py = -height/2
    #     a, b, c = self.calculate_function(x1, x2, py)
    #     POINTS_NUM = int(width)
    #     self.parabola_points = []
    #     self.inverted_parabola_points = []
    #     for i in range(int(-POINTS_NUM/2), int(POINTS_NUM/2)):
    #         x = (width/POINTS_NUM)*i
    #         y = a*x**2 + b*x + c + y_offset
    #
    #         inv_y = -a*x**2 + -b*x + c + y_offset + abs(rect_points[0][1] - rect_points[2][1])
    #         x += x_offset
    #         self.parabola_points.append((x, y))
    #         self.inverted_parabola_points.append((x, inv_y))
    #     center = (x_offset, y_offset)
    #     self.rect.center = center
    #     self.parabola_points = self.rotate_points2(self.parabola_points,90 + angle, center)
    #     self.inverted_parabola_points = self.rotate_points2(self.inverted_parabola_points, 90 + angle, center)

    def generate_arc_points(self, center, radius, start_angle, end_angle, num_points):
        points = []
        angle_step = (end_angle - start_angle) / num_points
        for i in range(num_points + 1):
            angle = start_angle + i * angle_step
            x = center[0] + int(radius * math.cos(angle))
            y = center[1] + int(radius * math.sin(angle))
            if functions.pointInRect((x, y), self.rect):
                points.append((x, y))
        return points

    def generate_points(self, rect_points, angle):
        x1 = rect_points[0][1]
        x2 = rect_points[2][1]
        height = abs(x1 - x2)
        width = abs(rect_points[0][0] - rect_points[2][0])
        POINTS_NUM = int(height)
        center = self.rect.center
        center_x = center[0]

        #pygame.draw.line(self.game.screen, (255, 255, 0),(rect_points[0][0] + width//2, rect_points[0][1] - 50),(rect_points[2][0] - width//2, rect_points[2][1] + 50), 5)

        self.lens_points = []

        # for i in range(POINTS_NUM):
        #     angle = 2 * math.pi * i / POINTS_NUM
        #     x = center[0] + int(self.curvature_radius * math.cos(angle))
        #     y = center[1] + int(self.curvature_radius * math.sin(angle))
        #     self.parabola_points.append((x, y))
        if self.type == self.CONVEX:
            center1 = (center_x + self.curvature_radius - width // 2, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius, math.pi/2, 3 * math.pi / 2, POINTS_NUM)
            center2 = (center_x - self.curvature_radius + width // 2, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius, -math.pi / 2, math.pi / 2, POINTS_NUM)
        else:
            center1 = (center_x + self.curvature_radius, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius, math.pi / 2, 3 * math.pi / 2,
                                                        POINTS_NUM)
            center2 = (center_x - self.curvature_radius, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius, -math.pi / 2, math.pi / 2,
                                                         POINTS_NUM)

        self.lens_points = self.rotate_points2(self.lens_points, angle, (center_x, center[1]))
        self.lens_points2 = self.rotate_points2(self.lens_points2, angle, (center_x, center[1]))
        center1 = self.rotate_points2([center1], angle, (center_x, center[1]))[0]
        pygame.draw.circle(self.game.screen, (0, 255, 0),
                           center1, 2, 0)
        center2 = self.rotate_points2([center2], angle, (center_x, center[1]))[0]
        pygame.draw.circle(self.game.screen, (0, 255, 0),
                          center2, 2, 0)



    def rotate_points2(self, points, angle, center):
        # Rotate points around the center of the object
        # center_x = sum(x for x, _ in points) / len(points)
        # center_y = sum(y for _, y in points) / len(points)

        center_x = center[0]
        center_y = center[1]

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

    def draw_convex(self, rect, angle):
        self.generate_points(rect, angle)

    def draw_concave(self, rect, angle):
        self.generate_points(rect, angle)

    def render(self):
        # print(self.get_triangles())

        self.get_slopes()


        if not self.selectedtrue:
            # Draw the rotated lines without transparency
            if self.texture:
                pygame.gfxdraw.textured_polygon(self.game.screen, self.points, self.texture, int(self.x), int(self.y))
            else:
                if self.type == self.CONVEX:
                    self.draw_convex(self.points, self.angle)
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                    pygame.gfxdraw.filled_polygon(self.game.screen, (self.lens_points[0], self.lens_points[-1], self.lens_points2[0], self.lens_points2[-1]), self.color)
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
                else:
                    self.draw_concave(self.points, self.angle)
                    # pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                    # pygame.gfxdraw.filled_polygon(self.game.screen, (
                    # self.lens_points[0], self.lens_points[-1], self.lens_points2[0], self.lens_points2[-1]), self.color)
                    # pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
                    pygame.draw.lines(self.game.screen, self.color, True, self.lens_points + self.lens_points2, 3)

        else:
            mousepos = pygame.mouse.get_pos()
            if self.game.r:

                self.adjust(mousepos[0], mousepos[1], self.game.r)
                self.game.r = False

            elif self.game.p:
                self.change_parameters()
                self.selectedtrue = False

            else:
                self.adjust(mousepos[0], mousepos[1], 0)
            if self.type == self.CONVEX:
                self.draw_convex(self.points, self.angle)
                pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                pygame.gfxdraw.filled_polygon(self.game.screen, (
                self.lens_points[0], self.lens_points[-1], self.lens_points2[0], self.lens_points2[-1]), self.color)
                pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
            else:
                self.draw_concave(self.points, self.angle)
                #pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                # length = len(self.lens_points)//2
                # lens_points = []
                # for point in self.lens_points:

                #pygame.gfxdraw.filled_polygon(self.game.screen, lens_points, self.color)
                pygame.draw.lines(self.game.screen, self.color, True, self.lens_points + self.lens_points2, 3)
                #pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)

            self.drawoutline()
    def adjust(self, x, y, d_angle):
        # Adjust the object's position and angle
        self.angle += d_angle
        self.x = x - sum(pt[0] for pt in self.points) / len(self.points)
        self.y = y - sum(pt[1] for pt in self.points) / len(self.points)

        # Reset the flag to regenerate triangles
        self.triangles_generated = False

        # Update the points based on the new position and angle
        #self.points = self.rotate_points(self.points, d_angle)

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
            #self.update_rect()

        else:
            self.points = [(x + self.x, y + self.y) for x, y in self.points]
            mousepos = pygame.mouse.get_pos()
            if self.texture:
                pygame.gfxdraw.textured_polygon(self.game.screen, self.points, self.texture, mousepos[0], -mousepos[1])
            # else:
                # pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)
            self.update_rect()
    def update_rect(self):
        # Update the rect based on the points
        min_x = min(pt[0] for pt in self.points)
        min_y = min(pt[1] for pt in self.points)
        max_x = max(pt[0] for pt in self.points)
        max_y = max(pt[1] for pt in self.points)
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

class Flashlight(GameObject):  # Inheriting from GameObject
    def __init__(self, game, points, color, angle, reflection_factor, islighting=True, image=None):
        super().__init__(game, points, color, angle, reflection_factor, image)
        self.islighting = bool(islighting)
        self.light = None
        self.light_width = 8
        self.color = color
        self.angle = angle
        self.image = image if image else None
        self.lazer = False
        self.rays = []

    def render(self):

        if not self.lazer:
            super().render()
            if self.islighting:
                #surface = pygame.surface.Surface(self.game.screen.get_size()).convert_alpha()
                #surface.fill([0, 0, 0, 0])
                if self.on:
                    ray_angle = self.angle - HALF_FOV + 0.0001
                    # Calculate the starting point of the light from the center of the rotated rectangle/surface
                    center_x = sum(x for x, _ in self.points) / len(self.points)
                    center_y = sum(y for _, y in self.points) / len(self.points)
                    self.light_adjust(center_x, center_y)
                    # if up arrow clicked, color goes random
                    if pygame.key.get_pressed()[pygame.K_UP]:
                        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    for ray in range(NUM_RAYS):
                        # self.light = light.Light(self.game,
                        #                          [[self.light_start_x, self.light_start_y]],
                        #                          self.color, -1*self.angle, self.light_width)
                        self.light = light.Light(self.game,
                                                 [[self.light_start_x, self.light_start_y]],
                                                 self.color, -1 * ray_angle, self.light_width, alpha=40)
                        #self.light.angle = -1 * ray_angle

                        self.light.trace_path2()
                        self.placed = True
                        # self.light = light.Light(self.game, ((self.light_start_x, self.light_start_y), (self.light_end_x, self.light_end_y)),"white", self.angle, self.light_width)

                        # Render the light before blitting the rotated surface
                        #light.Light.render(self.light, surface)
                        light.Light.render(self.light)
                        #self.game.objects.remove(self.light)
                        ray_angle += DELTA_ANGLE
                    super().render()
                    #self.game.screen.blit(surface, (0, 0))

                elif not self.on:
                    self.light = None
        else:
            super().render()
            if self.islighting:
                if self.on:
                    # Calculate the starting point of the light from the center of the rotated rectangle/surface
                    center_x = sum(x for x, _ in self.points) / len(self.points)
                    center_y = sum(y for _, y in self.points) / len(self.points)
                    self.light_adjust(center_x, center_y)
                    if pygame.key.get_pressed()[pygame.K_UP]:
                        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    self.light = light.Light(self.game,
                                             [[self.light_start_x, self.light_start_y]],
                                             self.color, -1 * self.angle, self.light_width, alpha=40)

                    # if up arrow clicked, color goes random

                    self.light.trace_path2()
                    self.placed = True
                    light.Light.render(self.light)
                    super().render()

                elif not self.on:
                    self.light = None


    def light_adjust(self, center_x, center_y):

        if not self.lazer:
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
        else:
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
