import classes.game
import functions
import pygame
from gui import ModifyParameters as mp
from gui import gui_main
from classes import light, mixer_c, images
import math
from pygame.transform import rotate
import random
import settingsSetup
from pygame import gfxdraw
from classes.font import Font
settings = settingsSetup.start()

NUM_RAYS = settings['Flashlight_Rays']
FOV = settings['Flashlight_FOV']
HALF_FOV = FOV / 2
DELTA_ANGLE = FOV / NUM_RAYS

class GameObject:

    def __init__(self, game, points, color, angle, transmittance, absorbsion_factor, image = None):
        # Initialize common attributes
        self.game = game
        self.color = color
        self.defualt_points = points

        self.points = self.defualt_points


        # self.get_Texture()

        #self.color = color if not self.texture else None

        self.on = True
        self.selectedtrue = False
        self.mousepos = None
        self.layer = 0
        self.placed = False
        self.angle = angle


        self.image = image if image else None
        self.resizing = False
        self.resize_rects = []
        self.resize_on = False
        self.resize_point = None

        self.absorbsion_factor = absorbsion_factor
        self.orginal_transmittance = transmittance
        self.set_transmittence()


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
        self.change_parameters('afdsf')

        self.was_selected = False
        self.collisionDetected = True
        mousepos = pygame.mouse.get_pos()
        self.adjust(mousepos[0], mousepos[1], self.angle)

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

    def draw_Poly(self):
        pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)

    def checkResize(self):
        if self.resizing and isinstance(self, Mirror):
            return self.points
        else:
            return False

    def render(self):

        if self.game.readyToCheck != False:
            self.collisionDetected = False
            for obj in self.game.objects:
                if self.game.readyToCheck != False:
                    if type(obj) != light.Light:
                        try:
                            print('trying')
                            if obj.rect.colliderect(pygame.Rect(self.game.readyToCheck)):
                                print('goodcolide')
                                self.collisionDetected = True
                                self.game.readyToCheck = False

                        except:
                            print(' wrong')
            if not self.collisionDetected:
                self.game.readyToCheck = False
                self.game.createPoly(True)

        # print(self.get_triangles())

        self.get_slopes()

        # print(self.points)

        if not self.selectedtrue:
            if self.resizing:
                self.drawResizeOutline()
                pass
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
                if self.color:
                    try:
                        pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)
                    except Exception as e:

                        # print(self.points)
                        print(e)
                else:
                    pygame.gfxdraw.polygon(self.game.screen, self.points, (255, 255, 255))

        else:
            # font = pygame.font.Font(Font, self.game.width//40)
            #
            # text = font.render('Click P to open parameters window', True, (255, 255, 255))
            #
            # text_rect = text.get_rect()
            #
            # text_rect.centerx = self.game.screen.get_rect().centerx
            # text_rect.y = 10
            #
            # self.game.screen.blit(text, text_rect)
            mousepos = pygame.mouse.get_pos()
            if self.game.r:

                self.adjust(mousepos[0], mousepos[1], self.game.r)
                self.game.r = False

            elif self.game.p:
                self.change_parameters()
                self.game.selected_object = None
                self.game.achievements.handle_achievement_unlocked("you just found more options")
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
    # def get_slopes_rect(self,rect):
    #     slopes = [(rect.points[i], rect.points[i + 1]) for i in range(len(self.points) - 1)]
    #     slopes.append((self.points[len(self.points) - 1], self.points[0]))
    def adjust(self, x, y, d_angle):
        while True:
            if self.angle >= 360:
                self.angle -= 360
            elif self.angle < 0:
                self.angle += 360
            else:
                break



        if self.game.isDrawingModeOn != True:
            # print(self.points)
            self.angle += d_angle
            self.x = x - sum(pt[0] for pt in self.points) / len(self.points)
            self.y = y - sum(pt[1] for pt in self.points) / len(self.points)

            # print(self.x)
            newpoints=[]
            oldpoints=self.points
            temp_rect = self.rect.move(self.x, self.y)
            for point in self.points:
                newpoints.append((point[0]+self.x,point[1]+self.y))
            self.points=newpoints
            self.get_slopes()
            for obj in self.game.objects:

                    if obj != self and isinstance(obj, GameObject):
                        # if obj.rect.colliderect(temp_rect):
                        obj.get_slopes()

                        slopes=obj.slopes
                        for s1 in self.slopes:
                            for s2 in slopes:
                                if (s1[0][0] - s1[1][0]) == 0:
                                    dx = 0.001
                                else:
                                    dx = (s1[0][0] - s1[1][0])
                                # r=math.atan((slope[0][0]-slope[1][0])/dy)

                                lf1 = light.Linear_Function((s1[0][1] - s1[1][1]) / dx,
                                                     self.find_b(((s1[0][1] - s1[1][1]) / dx), s1[0]))
                                lf1.draw(self.game)

                                # calculating second linear function:
                                if (s2[0][0] - s2[1][0]) == 0:
                                    dx = 0.001
                                else:
                                    dx = (s2[0][0] - s2[1][0])
                                # r=math.atan((slope[0][0]-slope[1][0])/dy)

                                lf2 = light.Linear_Function((s2[0][1] - s2[1][1]) / dx,
                                                     self.find_b(((s2[0][1] - s2[1][1]) / dx), s2[0]))
                                lf2.draw(self.game)
                                x = lf1.intercept(lf2)

                                y = lf1.calculate(x)
                                point = (x, lf1.calculate(x))


                                if (s1[0][0] - s1[1][0]) == 0:  # checking 'special case slope': |
                                    adding = 1
                                else:
                                    adding = 0
                                if x - adding <= max(s1[0][0], s1[1][0]) and x + adding >= min(s1[0][0],
                                                                                                     s1[1][0]):
                                    if y <= max(s1[0][1], s1[1][1]) and y >= min(s1[0][1], s1[1][1]):
                                        if x - adding <= max(s2[0][0], s2[1][0]) and x + adding >= min(s2[0][0],
                                                                                                       s2[1][0]):
                                            if y <= max(s2[0][1], s2[1][1]) and y >= min(s2[0][1], s2[1][1]):

                                                self.angle -= d_angle
                                                pygame.draw.circle(self.game.screen, (255, 0, 0), (x, y), 3)
                                                return




                        # elif isinstance(obj, gui_main.GUI):
                        #     self.angle -= d_angle
                        #     return
            self.points=oldpoints


            # print(temp_rect)

            pygame.gfxdraw.rectangle(self.game.screen, temp_rect, (255, 255, 255))



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
                try:
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)
                except:
                    pass
                self.update_rect()
    def find_b(self,a,point):
        return point[1]-a*point[0]
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
            pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)

    def drawoutline(self):
        # Draw an outline around the object
        pygame.gfxdraw.aapolygon(self.game.screen, self.points, (255, 255, 255))
        if settings['DEBUG'] == "True":
            pygame.draw.rect(self.game.screen, (255, 255, 0), self.rect, 2) # draw object hitbox
    def checkIfNormalMirror(self):
        x, y = [], []
        maxi, mini = 0, 0

        if len(self.points) == 4:
            for i in self.points:
                x.append(i[0])
                y.append(i[1])

            maxi, mini = max(x), min(x)
            maxCounter, minCounter = 0, 0
            for i in self.points:
                if i[0] == maxi:
                    maxCounter += 1
                elif i[0] == mini:
                    minCounter += 1
                else:
                    return False
            if minCounter == 2 and maxCounter == 2:
                maxi, mini = max(y), min(y)
                maxCounter, minCounter = 0, 0
                for i in self.points:
                    if i[1] == maxi:
                        maxCounter += 1
                    elif i[1] == mini:
                        minCounter += 1
                    else:
                        return False
                if minCounter == 2 and maxCounter == 2:
                    return True
            else:
                return False
        else:
            return False

    def drawResizeOutline(self):
        if isinstance(self, Mirror) and not self.checkIfNormalMirror():
            print(self.checkIfNormalMirror())
            classes.game.Game.movePoints(self.game, self.points, pygame.mouse.get_pos())
        elif not isinstance(self, Flashlight):
            print(self.checkIfNormalMirror())
            # Draw an outline around the object
            pygame.gfxdraw.aapolygon(self.game.screen, self.points, (255, 255, 255))
            self.resize_rects = []
            for point in self.points:
                rect = pygame.Rect(point[0] - 10, point[1] - 10, 20, 20)
                pygame.draw.rect(self.game.screen, (245, 212, 24), rect, border_radius=5)
                self.resize_rects.append(rect)
            if self.resize_on:
                try:
                    self.points[self.x_resize_index] = (pygame.mouse.get_pos()[0], self.points[self.x_resize_index][1])
                    #pygame.draw.circle(self.game.screen, (255, 0, 0), self.points[self.x_resize_index], 5)
                    self.points[self.y_resize_index] = (self.points[self.y_resize_index][0], pygame.mouse.get_pos()[1])
                    #pygame.draw.circle(self.game.screen, (0, 255, 0), self.points[self.y_resize_index], 5)
                    self.points[self.resize_point_index] = pygame.mouse.get_pos()
                    #pygame.draw.circle(self.game.screen, (0, 0, 255), self.points[self.resize_point_index], 5)
                except:
                    print(1)


            if settings['DEBUG'] == "True":
                pygame.draw.rect(self.game.screen, (255, 255, 0), self.rect, 2) # draw object hitbox

    def checkifclicked(self, mousepos):
        if self.game.isDrawingModeOn != True:
            # Check if the object is clicked
            mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
            pygame.gfxdraw.filled_polygon(mask_surface, self.points, (255, 255, 255))
            try:
                if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0:
                    if self.on == 1:
                        self.on = 0
                    else:
                        self.on = 1
            except IndexError: #pixel index out of range... WTF
                if self.on == 1:
                    self.on = 0
                else:
                    self.on = 1

    def selected(self, mousepos):
        if self.game.isDrawingModeOn != True:
            mask_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
            pygame.gfxdraw.filled_polygon(mask_surface, self.points, (255, 255, 255))

            if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0 and self.game.selected_object is not None and self.game.selected_object != self:
                self.game.selected_object.selectedtrue = False  # Deselect the currently selected object

            if mask_surface.get_at((int(mousepos[0]), int(mousepos[1])))[3] != 0 and not self.selectedtrue:
                if self.was_selected:
                    self.game.mixer.selected_sound()
                if self.was_selected == False:
                    self.was_selected = True
                self.selectedtrue = True
                self.game.selected_object = self  # Set this object as the currently selected object
            elif self.selectedtrue:
                if self.game.r_key:
                    if self.resizing is False:
                        self.resizing = True
                    else:
                        self.resizing = False
                self.selectedtrue = False
                self.game.selected_object = None  # No object is selected now
                if type(self) == Flashlight:
                    self.game.mixer.laser_sound()
                else:
                    self.game.mixer.placed_sound()


    def find_parameters(self):
        centerx = sum(x[0] for x in self.points) / len(self.points)
        centery = sum(y[1] for y in self.points) / len(self.points)
        # print('xxxxxxxxxxxx', centerx)

        self.parameters = {'x':centerx, 'y':centery, 'angle':self.angle}

        self.parameters['size'] = self.scale_factor

        # self.parameters['reflection_factor'] = self.reflection_factor
        if type(self) != Flashlight and type(self) != Lens:
            self.parameters['absorbsion_factor'] = self.absorbsion_factor

            self.parameters['transmittance'] = self.orginal_transmittance

        self.parameters['points'] = self.defualt_points
        # print(self.defualt_points)

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

        # print(self.parameters)

        self.defualt_points = self.parameters['points']
        self.points = self.defualt_points

        self.scale_factor = self.parameters['size']
        self.change_size()
        d_angle = self.parameters['angle']

        if d_angle==0:
            d_angle=0.001
        elif d_angle==180:
            d_angle=180.001
        elif d_angle==90:
            d_angle=90.001
        elif d_angle==270:
            d_angle=270.001
        self.angle = 0
        self.x = self.parameters['x']
        self.y = self.parameters['y']
        self.adjust(self.x, self.y, d_angle)
        self.scale_factor = self.parameters['size']
        try:
            self.absorbsion_factor = self.parameters['absorbsion_factor']
            self.orginal_transmittance = self.parameters['transmittance']
            self.set_transmittence()
        except:
            pass

        # print('a', self.absorbsion_factor, 't', self.transmittance, self.parameters['transmittance'], 'r', self.reflection_factor)

        try:
            self.color = (self.parameters['red'], self.parameters['green'], self.parameters['blue'])
            # self.get_Texture()

        except Exception as e:
            print(e)

        try:
            self.lazer = self.parameters["lazer"]
        except Exception as e:
            print(e)

    # def get_Texture(self):
    #     if self.textureName == 'wood':
    #         self.texture = images.wood
    #     elif self.textureName == 'glass':
    #         self.texture = images.glass
    #     elif self.textureName == 'water':
    #         self.texture = images.water
    #     elif self.textureName == 'clouds':
    #         self.texture = images.clouds
    #     elif self.textureName == 'paper':
    #         self.texture = images.papier
    #     else:
    #         self.texture = None

    def change_size(self):

        percent = self.scale_factor

        new_points = []

        for point in self.defualt_points:
            new_x = ((point[0] - float(self.parameters['x'])) * percent) + float(self.parameters['x'])
            new_y = (point[1] - float(self.parameters['y'])) * percent + float(self.parameters['y'])

            new_points.append((new_x, new_y))
        self.points = new_points

    def set_transmittence(self):
        self.transmittance = self.orginal_transmittance * (1 - self.absorbsion_factor)  # przepuszczalność ;-;
        self.reflection_factor = (1 - self.orginal_transmittance) * (1 - self.absorbsion_factor)


class Mirror(GameObject):
    def __init__(self, game, points, color, angle, transmittance, absorbsion_factor, islighting=False, image_path=None):
        super().__init__(game, points, color, angle, transmittance, absorbsion_factor, image_path)

class Prism(GameObject):
    def __init__(self, game, points, color, angle, transmittance, absorbsion_factor, islighting=False, image_path=None):
        super().__init__(game, points, color, angle, transmittance, absorbsion_factor, image_path)
        self.n=1.52
        self.fi=math.pi/3
        self.dispersion_angle=math.pi/3
    def get_left_wall(self):
        xs=[point[0] for point in self.points]
        ys=[point[1] for point in self.points]
        self.get_slopes()
        for slope in self.slopes:
            a=True
            for point in slope:
                if max(xs) in point:
                    a=False
            if a:
                self.left_slope=slope
        pygame.draw.line(self.game.screen, (255, 0, 0), self.left_slope[0], self.left_slope[1], 5)
    def get_right_wall(self):
        xs=[point[0] for point in self.points]
        ys=[point[1] for point in self.points]
        self.get_slopes()
        for slope in self.slopes:
            a=True
            for point in slope:
                if min(xs) in point:
                    a=False
            if a:
                self.right_slope=slope
        pygame.draw.line(self.game.screen, (0, 255, 255), self.right_slope[0], self.right_slope[1], 5)
    def get_bottom_wall(self):
        xs=[point[0] for point in self.points]
        ys=[point[1] for point in self.points]
        self.get_slopes()
        for slope in self.slopes:

            if (slope[0][0]==max(xs) and slope[1][0]==min(xs)) or (slope[1][0]==max(xs) and slope[0][0]==min(xs)):
                self.bottom_slope=slope
        pygame.draw.line(self.game.screen, (255, 255, 0), self.bottom_slope[0], self.bottom_slope[1], 5)

class ColoredGlass(GameObject):
    def __init__(self, game, points, color, angle, transmittance, absorbsion_factor, islighting=False, image_path=None):
        super().__init__(game, points, color, angle, transmittance, absorbsion_factor, image_path)
class CustomPolygon(GameObject):
    def __init__(self, game, points, color, angle, transmittance, absorbsion_factor, islighting=False, image_path=None, layer = 5):
        super().__init__(game, points, color, angle, transmittance, absorbsion_factor, image_path)
class Corridor(GameObject):
    def __init__(self, game, points, color, angle, transmittance, absorbsion_factor, islighting=False, image_path=None, layer = 5):
        super().__init__(game, points, color, angle, transmittance, absorbsion_factor, image_path)
    def get_slopes(self):
        self.slopes = [(self.points[2*i], self.points[2*i + 1]) for i in range((len(self.points))//2)]
        # self.slopes.append((self.points[len(self.points) - 1], self.points[0]))
        # print(self.slopes)

class Lens(GameObject):
    def __init__(self, game, points, color, angle, curvature_radius, transmittance, absorbsion_factor, curvature_radius2=None, refraction_index=1.5, islighting=False, image_path=None):
        super().__init__(game, points, color, angle, transmittance, absorbsion_factor, image_path)
        self.curvature_radius = curvature_radius
        self.CONVEX = 0
        self.CONCAVE = 1
        self.SINGLE_VEX = 2
        self.SINGLE_CAVE = 3
        self.VEX_CAVE = 4
        self.CAVE_VEX = 5
        self.SINGLE_VEX_2 = 6
        self.SINGLE_CAVE_2 = 7

        self.lens_points = []
        self.refraction_index = refraction_index
        self.layer = 0
        self.change_curvature_left = False
        self.change_curvature_right = False
        self.last_mouse_pos = None
        self.curvature_radius2 = None
        self.curvature_resize_step = 1
        self.DEFAULT_MARGIN = 20
        self.margin = self.DEFAULT_MARGIN
        self.raw_curvature_radius = self.curvature_radius
        self.raw_curvature_radius2 = self.curvature_radius2

        if curvature_radius2 is not None:
            self.curvature_radius2 = curvature_radius2
            self.raw_curvature_radius2 = curvature_radius
            if curvature_radius2 > 0 and curvature_radius > 0:
                self.type = self.CONVEX
            elif curvature_radius < 0 and curvature_radius2 < 0:
                self.type = self.CONCAVE
                self.curvature_radius = -self.curvature_radius
                self.curvature_radius2 = -curvature_radius2
            elif curvature_radius < 0 and curvature_radius2 > 0:
                self.type = self.CAVE_VEX
                self.curvature_radius = -self.curvature_radius
            elif curvature_radius > 0 and curvature_radius2 < 0:
                self.type = self.VEX_CAVE
                self.curvature_radius2 = -curvature_radius2
        elif curvature_radius > 0:
            self.type = self.SINGLE_VEX
        elif curvature_radius < 0:
            self.type = self.SINGLE_CAVE
            self.curvature_radius = -curvature_radius

    def checktype(self):
        if self.raw_curvature_radius2 is not None and self.raw_curvature_radius2 != 0:
            if self.raw_curvature_radius2 > 0 and self.raw_curvature_radius > 0:
                self.type = self.CONVEX
            elif self.raw_curvature_radius < 0 and self.raw_curvature_radius2 < 0:
                self.type = self.CONCAVE
                self.curvature_radius = -self.curvature_radius
                self.curvature_radius2 = -self.curvature_radius2
            elif self.raw_curvature_radius < 0 and self.raw_curvature_radius2 > 0:
                self.type = self.CAVE_VEX
                self.curvature_radius = -self.curvature_radius
            elif self.raw_curvature_radius > 0 and self.raw_curvature_radius2 < 0:
                self.type = self.VEX_CAVE
                self.curvature_radius2 = -self.curvature_radius2
            elif self.raw_curvature_radius == 0 and self.raw_curvature_radius2 > 0:
                self.type = self.SINGLE_VEX_2
            elif self.raw_curvature_radius == 0 and self.raw_curvature_radius2 < 0:
                #self.curvature_radius = self.curvature_radius2
                self.type = self.SINGLE_CAVE
        elif self.raw_curvature_radius > 0:
            self.type = self.SINGLE_VEX
        elif self.raw_curvature_radius < 0:
            self.type = self.SINGLE_CAVE_2
            #self.curvature_radius = -self.curvature_radius



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
        self.height = abs(x1 - x2)
        self.width = abs(rect_points[0][0] - rect_points[2][0])
        POINTS_NUM = int(self.height) * 2
        points_num1 = POINTS_NUM
        if self.curvature_radius * 2 > POINTS_NUM:
            points_num1 = self.curvature_radius * 2
        points_num2 = POINTS_NUM
        if self.curvature_radius2 is not None:
            if self.curvature_radius2 * 2 > POINTS_NUM:
                    points_num2 = self.curvature_radius2 * 2
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
            center1 = (center_x + self.curvature_radius - self.width // 2, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius, math.pi/2, 3 * math.pi / 2, points_num1)
            center2 = (center_x - self.curvature_radius2 + self.width // 2, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius2, -math.pi / 2, math.pi / 2, points_num2)
        elif self.type == self.SINGLE_VEX:
            center1 = (center_x + self.curvature_radius - self.width // 2, center[1])
            center2 = (center_x - self.curvature_radius, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius, math.pi/2, 3 * math.pi / 2, points_num1)
            self.lens_points2 = []
            for i in range(POINTS_NUM):
                self.lens_points2.append((center_x, center[1] - self.height/2 + i * (self.height / POINTS_NUM)))
        elif self.type == self.SINGLE_VEX_2:
            center1 = (center_x + self.curvature_radius2, center[1])
            center2 = (center_x - self.curvature_radius2 + self.width // 2, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius2, -math.pi / 2, math.pi / 2, points_num2)
            self.lens_points = []
            for i in range(POINTS_NUM):
                self.lens_points.append((center_x, center[1] - self.height/2 + i * (self.height / POINTS_NUM)))
        elif self.type == self.SINGLE_CAVE:
            center1 = (center_x + self.curvature_radius, center[1])
            center2 = (center_x - self.curvature_radius, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius, math.pi / 2, 3 * math.pi / 2,
                                                        points_num1)
            self.lens_points2 = []
            for i in range(POINTS_NUM):
                self.lens_points2.append((center_x, center[1] - self.height/2 + i*(self.height / POINTS_NUM)))
        elif self.type == self.SINGLE_CAVE_2:
            center1 = (center_x + self.curvature_radius, center[1])
            center2 = (center_x - self.curvature_radius, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius, -math.pi / 2, math.pi / 2,
                                                        points_num2)
            self.lens_points = []
            for i in range(POINTS_NUM):
                self.lens_points.append((center_x, center[1] - self.height/2 + i*(self.height / POINTS_NUM)))
        elif self.type == self.CONCAVE:
            center1 = (center_x + self.curvature_radius2, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius2, math.pi / 2, 3 * math.pi / 2,
                                                        points_num1)
            center2 = (center_x - self.curvature_radius, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius, -math.pi / 2, math.pi / 2,
                                                         points_num2)
        elif self.type == self.CAVE_VEX:
            center1 = (center_x - self.curvature_radius2 + self.width // 2, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius2, -math.pi / 2, math.pi / 2,
                                                        points_num1)
            #print(self.lens_points)
            center2 = (center_x - self.curvature_radius, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius, -math.pi / 2, math.pi / 2,
                                                         points_num2)
        elif self.type == self.VEX_CAVE:
            center1 = (center_x + self.curvature_radius2, center[1])
            self.lens_points = self.generate_arc_points(center1, self.curvature_radius2, math.pi / 2, 3 * math.pi / 2,
                                                        points_num1)
            # print(self.lens_points)
            center2 = (center_x + self.curvature_radius - self.width // 2, center[1])
            self.lens_points2 = self.generate_arc_points(center2, self.curvature_radius, math.pi / 2, 3 * math.pi / 2,
                                                        points_num2)

        # self.lens_points = self.rotate_points2(self.lens_points, angle, (center_x, center[1]))
        # self.lens_points2 = self.rotate_points2(self.lens_points2, angle, (center_x, center[1]))
        # self.center1 = self.rotate_points2([center1], angle, (center_x, center[1]))[0]
        # pygame.draw.circle(self.game.screen, (0, 255, 0),
        #                    self.center1, 2, 0)
        # self.center2 = self.rotate_points2([center2], angle, (center_x, center[1]))[0]
        # pygame.draw.circle(self.game.screen, (0, 255, 0),
        #                   self.center2, 2, 0)
        #
        self.center1 = center1
        self.center2 = center2

    def drawResizeOutline(self):
        # Draw an outline around the object
        self.angle = 0
        pygame.gfxdraw.aapolygon(self.game.screen, self.points, (255, 255, 255))
        self.resize_rects = []
        for point in self.points:
            rect = pygame.Rect(point[0] - 10, point[1] - 10, 20, 20)
            pygame.draw.rect(self.game.screen, (245, 212, 24), rect, border_radius=5)
            self.resize_rects.append(rect)
        self.resize_rects.append(pygame.Rect(self.points[0][0] - 10, self.points[0][1] + self.height/2 - 10, 20, 20))
        pygame.draw.rect(self.game.screen, (245, 212, 24), self.resize_rects[-1], border_radius=5)
        mouse_pos = pygame.mouse.get_pos()
        self.resize_rects.append(pygame.Rect(self.points[1][0] - 10, self.points[1][1] + self.height / 2 - 10, 20, 20))
        pygame.draw.rect(self.game.screen, (245, 212, 24), self.resize_rects[-1], border_radius=5)

        if self.resize_on:
            if abs(self.points[self.static_point_index][0] - self.points[self.resize_point_index][0]) > 25 and abs(self.points[self.static_point_index][1] - self.points[self.resize_point_index][1]) > 25:
                self.points[self.x_resize_index] = (mouse_pos[0], self.points[self.x_resize_index][1])
                #pygame.draw.circle(self.game.screen, (255, 0, 0), self.points[self.x_resize_index], 5)
                self.points[self.y_resize_index] = (self.points[self.y_resize_index][0], mouse_pos[1])
                #pygame.draw.circle(self.game.screen, (0, 255, 0), self.points[self.y_resize_index], 5)
                self.points[self.resize_point_index] = mouse_pos
                #pygame.draw.circle(self.game.screen, (0, 0, 255), self.points[self.resize_point_index], 5)
            else:
                pass
                # temp = self.points[self.static_point_index][0]
                # self.points[self.static_point_index] = (temp + self.points[self.resize_point_index][0], self.points[self.static_point_index][1])
                # self.points[self.resize_point_index] = (self.points[self.resize_point_index][0] + temp, self.points[self.static_point_index][1])


        ### Checks if the lenses dont overlap ###
        if self.type == self.CONVEX:
            if self.lens_points2[-1][1] - self.lens_points2[0][1] < self.height -5:
                #self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
                self.curvature_radius2 += self.curvature_resize_step
            if self.lens_points2[0][0] < self.lens_points[0][0]:
                self.curvature_radius2 += self.curvature_resize_step
                #self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
            if self.lens_points[0][1] - self.lens_points[-1][1] < self.height -5:
                self.curvature_radius += self.curvature_resize_step
            if self.lens_points2[0][0] < self.lens_points[0][0]:
                self.curvature_radius += self.curvature_resize_step
        if self.type == self.SINGLE_VEX:
            if self.curvature_radius < self.height // 2 + 10:
                self.curvature_radius += self.curvature_resize_step
            if self.lens_points[0][1] - self.lens_points[-1][1] < self.height - 5:
                self.curvature_radius += self.curvature_resize_step
            if self.lens_points2[0][0] < self.lens_points[0][0] + 10:
                self.curvature_radius += self.curvature_resize_step
            if self.lens_points[0][1] <= self.lens_points2[0][1] - 20:
                self.curvature_radius = self.height//2
        if self.type == self.SINGLE_VEX_2:
            if self.curvature_radius2 < self.height // 2 + 10:
                self.curvature_radius2 += self.curvature_resize_step
            if self.lens_points2[-1][1] - self.lens_points2[0][1] < self.height -5:
                #self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
                self.curvature_radius2 += self.curvature_resize_step
            if self.lens_points2[0][0] < self.lens_points[0][0] + 10:
                self.curvature_radius2 += self.curvature_resize_step
            if self.lens_points[0][1] <= self.lens_points2[0][1] - 20:
                self.curvature_radius2 = self.height // 2
        if self.type == self.CONCAVE:
            if self.lens_points2[-1][1] - self.lens_points2[0][1] < self.height - 5:
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
                self.curvature_radius += self.curvature_resize_step
            #print(self.curvature_radius2)
            if self.lens_points2[0][0] > self.lens_points[0][0]:
                self.curvature_radius += self.curvature_resize_step
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
            if self.lens_points[-1][1] - self.lens_points[0][1] < self.height - 5:
                # print(self.lens_points[-1][1] - self.lens_points[0][1])
                self.curvature_radius2 += self.curvature_resize_step
            if self.lens_points2[0][0] > self.lens_points[0][0]:
                self.curvature_radius2 += self.curvature_resize_step
        if self.type == self.SINGLE_CAVE:
            if self.lens_points[0][1] - self.lens_points[-1][1] < self.height - 5:
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
                self.curvature_radius += self.curvature_resize_step
            #print(self.curvature_radius2)
            if self.lens_points2[0][0] > self.lens_points[0][0]:
                self.curvature_radius += self.curvature_resize_step
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
        if self.type == self.SINGLE_CAVE_2:
            if abs(self.lens_points2[0][1] - self.lens_points2[-1][1]) < self.height - 5:
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
                self.curvature_radius += self.curvature_resize_step
            #print(self.curvature_radius2)
            if self.lens_points2[0][0] > self.lens_points[0][0]:
                self.curvature_radius += self.curvature_resize_step
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
        if self.type == self.VEX_CAVE or self.type == self.CAVE_VEX:
            if abs(self.lens_points2[-1][1] - self.lens_points2[0][1]) < self.height - 5:
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
                self.curvature_radius += self.curvature_resize_step
            # print(self.curvature_radius2)
            if self.lens_points2[0][0] > self.lens_points[0][0]:
                self.curvature_radius += self.curvature_resize_step
                # self.curvature_radius2 = int(self.center2[0] - self.center1[0] - self.curvature_radius)
            if self.lens_points[-1][1] - self.lens_points[0][1] < self.height - 5:
                # print(self.lens_points[-1][1] - self.lens_points[0][1])
                self.curvature_radius2 += self.curvature_resize_step
            if self.lens_points2[0][0] > self.lens_points[0][0]:
                self.curvature_radius2 += self.curvature_resize_step


        if self.change_curvature_left:
            if self.type == self.CONVEX or self.type == self.SINGLE_VEX or self.type == self.VEX_CAVE: # left side is convex
                if self.type != self.VEX_CAVE:
                    if mouse_pos[0] > self.last_mouse_pos[0]:
                        if self.lens_points2[0][0] > self.lens_points[0][0] and self.lens_points[0][1] - self.lens_points[-1][1] > self.height -5:
                            self.curvature_radius -= self.curvature_resize_step
                        else:
                            self.curvature_radius = 0
                            self.raw_curvature_radius = 0
                            self.checktype()
                    if mouse_pos[0] < self.last_mouse_pos[0]:
                        self.curvature_radius += self.curvature_resize_step
                else:
                    if mouse_pos[0] > self.last_mouse_pos[0]:
                        if self.lens_points2[0][0] < self.lens_points[0][0] and self.lens_points[-1][1] - self.lens_points[0][1] > self.height -5:
                            self.curvature_radius -= self.curvature_resize_step
                        else:
                            self.raw_curvature_radius = 0
                            self.raw_curvature_radius2 = - self.curvature_radius2
                            self.curvature_radius = self.curvature_radius2
                            self.checktype()
                    if mouse_pos[0] < self.last_mouse_pos[0]:
                        self.curvature_radius += self.curvature_resize_step

            elif self.type == self.SINGLE_VEX_2 or self.type == self.SINGLE_CAVE: # left side is flat
                #print(self.margin)
                if mouse_pos[0] > self.last_mouse_pos[0]:
                    if self.margin > self.DEFAULT_MARGIN:
                        self.margin = self.DEFAULT_MARGIN
                    self.margin -= 1
                    if self.margin < 1:
                        if self.type == self.SINGLE_CAVE:
                            self.curvature_radius = -self.curvature_radius2
                            self.curvature_radius2 = - self.curvature_radius2
                            self.raw_curvature_radius = self.curvature_radius
                        else:
                            self.curvature_radius = -self.curvature_radius2
                            self.raw_curvature_radius = self.curvature_radius
                        self.checktype()
                        self.margin = self.DEFAULT_MARGIN
                if mouse_pos[0] < self.last_mouse_pos[0]:
                    if self.margin < self.DEFAULT_MARGIN:
                        self.margin = self.DEFAULT_MARGIN
                    self.margin += 1
                    if self.margin > 2*self.DEFAULT_MARGIN - 1:
                        if self.type == self.SINGLE_CAVE:
                            self.curvature_radius2 = -self.curvature_radius
                            self.raw_curvature_radius2 = -self.curvature_radius
                            self.raw_curvature_radius = self.curvature_radius

                        else:
                            self.curvature_radius = self.curvature_radius2
                            self.raw_curvature_radius = self.curvature_radius
                        self.checktype()
                        self.margin = self.DEFAULT_MARGIN
            elif self.type == self.CAVE_VEX or self.type == self.CONCAVE or self.type == self.SINGLE_CAVE_2: # left side is concave
                if mouse_pos[0] < self.last_mouse_pos[0]:

                    if self.lens_points2[0][0] < self.lens_points[0][0] and abs(self.lens_points2[-1][1] - self.lens_points2[0][1]) > self.height -5:
                        # print(self.type == self.SINGLE_CAVE_2)
                        # if self.type == self.SINGLE_CAVE_2:
                        #     self.curvature_radius -= self.curvature_resize_step
                        # else:
                            self.curvature_radius -= self.curvature_resize_step
                    else:
                        if self.type == self.SINGLE_CAVE_2:
                            self.curvature_radius2 = 0
                            self.raw_curvature_radius2 = self.curvature_radius2
                        else:
                            if self.type == self.CONCAVE:
                                self.raw_curvature_radius = 0
                                self.raw_curvature_radius2 = - self.curvature_radius2
                                self.curvature_radius = self.curvature_radius2
                            else:
                                self.curvature_radius = 0
                                self.raw_curvature_radius = self.curvature_radius
                        self.checktype()
                        print(self.type)
                if mouse_pos[0] > self.last_mouse_pos[0]:
                    # if self.type == self.SINGLE_CAVE_2:
                    #     self.curvature_radius2 += self.curvature_resize_step
                    # else:
                        self.curvature_radius += self.curvature_resize_step

        if self.change_curvature_right:
            if self.type == self.CONVEX or self.type == self.SINGLE_VEX_2 or self.type == self.CAVE_VEX:  # right side is convex
                if self.type != self.CAVE_VEX:
                    if mouse_pos[0] < self.last_mouse_pos[0]:
                        if self.lens_points2[0][0] > self.lens_points[0][0] and self.lens_points[0][1] - self.lens_points[-1][1] > self.height - 5:
                            self.curvature_radius2 -= self.curvature_resize_step
                        else:
                            self.curvature_radius2 = 0
                            self.raw_curvature_radius2 = 0
                            self.checktype()
                    if mouse_pos[0] > self.last_mouse_pos[0]:
                        self.curvature_radius2 += self.curvature_resize_step
                else:
                    if mouse_pos[0] < self.last_mouse_pos[0]:
                        if self.lens_points2[0][0] < self.lens_points[0][0] and self.lens_points[-1][1] - self.lens_points[0][1] > self.height -5:
                            self.curvature_radius2 -= self.curvature_resize_step
                        else:
                            self.curvature_radius2 = 0
                            self.raw_curvature_radius2 = 0
                            #self.curvature_radius = -self.curvature_radius
                            self.checktype()
                    if mouse_pos[0] > self.last_mouse_pos[0]:
                        self.curvature_radius2 += self.curvature_resize_step
            elif self.type == self.SINGLE_VEX or self.type == self.SINGLE_CAVE_2:  # right side is flat
                if mouse_pos[0] < self.last_mouse_pos[0]:
                    if self.margin > self.DEFAULT_MARGIN:
                        self.margin = self.DEFAULT_MARGIN
                    self.margin -= 1
                    if self.margin < 1:
                        if self.type == self.SINGLE_CAVE_2:
                            self.curvature_radius = -self.curvature_radius
                            self.curvature_radius2 = self.curvature_radius
                            self.raw_curvature_radius2 = self.raw_curvature_radius
                        else:
                            self.curvature_radius2 = -self.curvature_radius
                            self.raw_curvature_radius2 = self.curvature_radius2
                        self.checktype()
                        self.margin = self.DEFAULT_MARGIN
                if mouse_pos[0] > self.last_mouse_pos[0]:
                    if self.margin < self.DEFAULT_MARGIN:
                        self.margin = self.DEFAULT_MARGIN
                    self.margin += 1
                    if self.margin > 2 * self.DEFAULT_MARGIN - 1:
                        if self.type == self.SINGLE_CAVE_2:
                            self.curvature_radius2 = self.curvature_radius
                            self.curvature_radius = -self.curvature_radius
                            self.raw_curvature_radius2 = -self.raw_curvature_radius
                        else:
                            self.curvature_radius2 = self.curvature_radius
                            self.raw_curvature_radius2 = self.curvature_radius2
                        self.checktype()
                        self.margin = self.DEFAULT_MARGIN
            elif self.type == self.VEX_CAVE or self.type == self.CONCAVE or self.type == self.SINGLE_CAVE:  # right side is concave
                if mouse_pos[0] > self.last_mouse_pos[0]:
                    if self.lens_points2[0][0] < self.lens_points[0][0] and abs(self.lens_points[-1][1] - self.lens_points[0][1]) > self.height - 5:
                        if self.type == self.SINGLE_CAVE:
                            self.curvature_radius -= self.curvature_resize_step
                        else:
                            self.curvature_radius2 -= self.curvature_resize_step
                    else:
                        self.curvature_radius2 = 0
                        self.raw_curvature_radius2 = self.curvature_radius2
                        self.checktype()
                if mouse_pos[0] < self.last_mouse_pos[0]:
                    if self.type == self.SINGLE_CAVE:
                        self.curvature_radius += self.curvature_resize_step
                    else:
                        self.curvature_radius2 += self.curvature_resize_step
            # if mouse_pos[0] > self.last_mouse_pos[0]:
            #     if self.lens_points2[0][0] > self.lens_points[0][0] and self.lens_points2[-1][1] - self.lens_points2[0][1] > self.height -5:
            #         self.curvature_radius2 -= self.curvature_resize_step
            #     else:
            #         self.curvature_radius2 = 0
            #         self.raw_curvature_radius2 = self.curvature_radius2
            #         self.checktype()
            #         print(self.type)
            # if mouse_pos[0] < self.last_mouse_pos[0]:
            #     self.curvature_radius2 += self.curvature_resize_step
        #print(self.curvature_radius)
        self.last_mouse_pos = mouse_pos
        self.update_rect()


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

    def render(self):
        # print(self.get_triangles())

        # self.get_slopes()
        if not self.selectedtrue:
            # Draw the rotated lines without transparency
            if self.resizing:
                self.drawResizeOutline()
                #print(self.type)
            if self.type != self.CONCAVE and self.type != self.SINGLE_CAVE and self.type != self.CAVE_VEX and self.type != self.SINGLE_CAVE_2 and self.type != self.VEX_CAVE:
                self.generate_points(self.points, self.angle)
                if self.type != self.SINGLE_VEX_2:
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                else:
                    self.lens_points.reverse()
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
                if self.type != self.SINGLE_VEX and self.type != self.SINGLE_VEX_2:
                    pygame.gfxdraw.filled_polygon(self.game.screen, (self.lens_points[0], self.lens_points[-1], self.lens_points2[0], self.lens_points2[-1]), self.color)
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
                if self.type == self.SINGLE_VEX or self.type == self.SINGLE_VEX_2:
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2 + [self.lens_points[0], self.lens_points[-1]], self.color)
            else:
                self.generate_points(self.points, self.angle)
                # pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                # pygame.gfxdraw.filled_polygon(self.game.screen, (
                # self.lens_points[0], self.lens_points[-1], self.lens_points2[0], self.lens_points2[-1]), self.color)
                # pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
                if self.type == self.SINGLE_CAVE_2:
                    self.lens_points.reverse()
                if self.type == self.CAVE_VEX or self.type == self.VEX_CAVE:
                    self.lens_points.reverse()
                pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points + self.lens_points2,
                                              self.color)
                if self.type == self.CONCAVE or self.type == self.CAVE_VEX or self.type == self.SINGLE_CAVE_2:
                    self.lens_points.reverse()
                    # self.lens_points2.reverse()
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
            if self.type != self.CONCAVE and self.type != self.SINGLE_CAVE and self.type != self.CAVE_VEX and self.type != self.SINGLE_CAVE_2 and self.type != self.VEX_CAVE:
                self.generate_points(self.points, self.angle)
                if self.type != self.SINGLE_VEX_2:
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                else:
                    self.lens_points.reverse()
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
                if self.type != self.SINGLE_VEX and self.type != self.SINGLE_VEX_2:
                    pygame.gfxdraw.filled_polygon(self.game.screen, (
                    self.lens_points[0], self.lens_points[-1], self.lens_points2[0], self.lens_points2[-1]), self.color)
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2, self.color)
                if self.type == self.SINGLE_VEX or self.type == self.SINGLE_VEX_2:
                    pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points2 + [self.lens_points[0], self.lens_points[-1]], self.color)
            else:
                self.generate_points(self.points, self.angle)
                #pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points, self.color)
                # length = len(self.lens_points)//2
                # lens_points = []
                # for point in self.lens_points:
                if self.type == self.SINGLE_CAVE_2:
                    self.lens_points.reverse()
                if self.type == self.CAVE_VEX or self.type == self.VEX_CAVE:
                    self.lens_points.reverse()
                pygame.gfxdraw.filled_polygon(self.game.screen, self.lens_points + self.lens_points2,
                                              self.color)
                if self.type == self.CONCAVE or self.type == self.CAVE_VEX or self.type == self.SINGLE_CAVE_2:
                    self.lens_points.reverse()
                    # self.lens_points2.reverse()

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
        temp_rect = self.rect.move(self.x, self.y)

        # print(temp_rect)

        pygame.gfxdraw.rectangle(self.game.screen, temp_rect, (255, 255, 255))

        for obj in self.game.objects:
            if type(obj) != light.Light:
                if obj.rect.colliderect(temp_rect):
                    if obj != self and isinstance(obj, GameObject):
                        self.angle -= d_angle
                        return

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
            # if self.texture:
            #     pygame.gfxdraw.textured_polygon(self.game.screen, self.points, self.texture, mousepos[0], -mousepos[1])
            # # else:
            #     # pygame.gfxdraw.filled_polygon(self.game.screen, self.points, self.color)
            self.update_rect()
    def update_rect(self):
        # Update the rect based on the points
        min_x = min(pt[0] for pt in self.points)
        min_y = min(pt[1] for pt in self.points)
        max_x = max(pt[0] for pt in self.points)
        max_y = max(pt[1] for pt in self.points)
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

class Flashlight(GameObject):  # Inheriting from GameObject
    def __init__(self, game, points, color, angle, transmittance, absorbsion_factor, islighting=True, image=None):
        super().__init__(game, points, color, angle, transmittance, absorbsion_factor, image)
        self.islighting = bool(islighting)
        self.light = None
        self.light_width = 8
        self.color = color
        self.angle = angle
        self.image = image if image else None
        self.lazer = True
        self.rays = []
        self.layer = 2

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
                        self.game.objects.append(self.light)
                        #self.game.objects.remove(self.light)
                        ray_angle += DELTA_ANGLE
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
                    # self.light.trace_path2()
                    self.placed = True
                    self.game.objects.append(self.light)

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
