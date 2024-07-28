import pygame
import math
from classes import gameobjects, fps
import time
import settingsSetup
import pygame.gfxdraw
import functions

from bigtree import Node


class Ray:
    def __init__(self, start_point, end_point, color):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.active = True


class Light:
    def __init__(self, game, points, color, angle, light_width, alpha=255):
        # points is a list that represents endpoints of next lines building a stream of light
        self.debug = False
        self.offset_r = 0
        self.difract_type = 'first'
        self.prism_light = False
        self.in_prism = False
        self.in_mirror = False
        self.main_light_slope = None
        self.linear_function = None
        self.starting_point = points[0]
        self.points = points
        self.game = game
        self.color = color
        self.angle = angle
        self.light_width = light_width
        self.layer = 1  # Assign a layer value to control rendering order
        # self.game.objects.insert(-1, self)
        self.colors = []
        self.RGB = RGB_Class(self.color[0], self.color[1], self.color[2])
        self.colors.append(self.RGB.rgb)
        self.x = self.points[0][0]
        self.y = self.points[0][1]
        self.count = 1
        self.get_r()
        self.alpha = alpha
        self.ignore_object = None
        self.counter = 0

        # print(self.r,self.linear_function)

    def find_b(self, a, point):
        return point[1] - a * point[0]

    def render(self):
        try:
            ### For RTX Flashlight ###
            if self.game.settings['HD_Flashlight'] == 'ON':
                #### Original ####
                # new_line_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
                # new_line_surface.set_alpha(self.alpha)
                for x in range(0, len(self.points) - 1):
                    #### Beta testing stuff ####
                    current_ray = Ray(self.points[x], self.points[x + 1], self.colors[x])
                    pointer = current_ray
                    isAdded = False
                    collisionless_layer = -1
                    for surface_num, rays in self.game.surface_rays.items():
                        collides = False
                        # if rays == [] and len(self.game.surfaces) >0:
                        #     self.game.surface_num -= 1
                        #     #self.game.surface_rays.pop(surface_num)
                        #     self.game.surfaces.pop()
                        for ray in rays:
                            if functions.do_lines_intersect(ray.start_point, ray.end_point, current_ray.start_point,
                                                            current_ray.end_point):
                                collides = True
                            if current_ray.start_point == ray.start_point and current_ray.end_point == ray.end_point:
                                isAdded = True
                                if ray.active == False:
                                    break
                        if collides is False:
                            collisionless_layer = surface_num
                    if isAdded is False:
                        if collisionless_layer != -1:
                            self.game.surface_rays[collisionless_layer].append(current_ray)
                        else:
                            # More efficient way, but kinda glitchy
                            self.game.surface_rays[max(self.game.surface_rays.keys())].append(current_ray)

                            # Unfinished optimal method

                            # self.game.surface_rays[max(self.game.surface_rays.keys()) + 1] = [current_ray]
                            # surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
                            # surface.set_alpha(40)
                            # self.game.surfaces.append(surface)
                            # self.game.surface_num += 1
                            # print("add")
                self.game.achievements.handle_achievement_unlocked("so you've chosen death")
                #### Original ####

                #     self.draw_thick_line(new_line_surface, int(self.points[x][0]), int(self.points[x][1]),
                #                         int(self.points[x + 1][0]), int(self.points[x + 1][1]), self.colors[x], 5)
                # self.game.screen.blit(new_line_surface, (0, 0))
            ### For Simple Flashlight ###
            else:
                for x in range(0, len(self.points) - 1):
                    self.draw_thick_line(self.game.screen, int(self.points[x][0]), int(self.points[x][1]),
                                         int(self.points[x + 1][0]), int(self.points[x + 1][1]), self.colors[x], 5)
            self.game.objects.remove(self)
        except (AttributeError, ValueError):
            pass

    # NON - RECURSIVE

    def special_case_adjust(self):
        if self.r == math.pi / 2:
            self.r = math.pi / 2 + 0.00001
        elif self.r == 3 * math.pi / 2:
            self.r = 3 * math.pi / 2 + 0.00001
        elif self.r == 0:
            self.r = 0.00001
        elif self.r == math.pi:
            self.r = math.pi + 0.00001

    def do_lines_intersect(self, p1, p2, p3, p4):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        if ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4):
            # Calculate intersection point
            denom = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
            if denom == 0:
                return False, None
            x = ((p1[0] * p2[1] - p1[1] * p2[0]) * (p3[0] - p4[0]) - (p1[0] - p2[0]) * (
                        p3[0] * p4[1] - p3[1] * p4[0])) / denom
            y = ((p1[0] * p2[1] - p1[1] * p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (
                        p3[0] * p4[1] - p3[1] * p4[0])) / denom
            print(x, y)
            return True, (x, y)
        return False, None

    def check_collision_with_other_lights(self, other_lights):
        for other_light in other_lights:
            if type(other_light) == Light and self != other_light:
                for i in range(len(self.points) - 1):
                    for j in range(len(other_light.points) - 1):
                        intersect, point = self.do_lines_intersect(self.points[i], self.points[i + 1], other_light.points[j], other_light.points[j + 1])
                        if intersect:
                            self.points.insert(-1, point)
                            other_light.points.insert(-1, point)

                            selfcolor = self.RGB.rgb
                            othercolor = other_light.RGB.rgb

                            color = ((selfcolor[0] + othercolor[0]) // 2, (selfcolor[1] + othercolor[1]) // 2, (selfcolor[2] + othercolor[2]) // 2)


                            print(color)

                            self.colors.insert(-1, color)
                            other_light.colors.insert(-1, color)


                            print(point)
                            break
    def trace_path2(self):
        if self.RGB.a > 0:
            self.current_starting_point = self.starting_point
            self.special_case_adjust()
            self.mini_run = True
            self.index = 0
            while self.mini_run:
                if self.r < math.pi:
                    self.vertical = 'up'
                else:
                    self.vertical = 'down'
                if self.r < 3 / 2 * math.pi and self.r > 1 / 2 * math.pi:
                    self.horizontal = 'left'
                else:
                    self.horizontal = 'right'
                self.index += 1
                self.linear_function = Linear_Function(math.tan(-self.r),
                                                       self.find_b(math.tan(-self.r), self.current_starting_point))
                if self.debug == True:
                    self.linear_function.draw(self.game)
                try:
                    self.slope_before = self.current_slope
                except:
                    self.slope_before = self.main_light_slope
                self.current_point_before = self.current_starting_point
                self.current_distance = None
                self.current_point = None
                self.current_slope = None
                self.current_object = None
                self.current_object_type = None
                lenses = []
                for object in self.game.objects:
                    if type(object) == gameobjects.Mirror or type(object) == gameobjects.ColoredGlass or type(
                            object) == gameobjects.Prism or type(object) == gameobjects.Corridor or type(object) == gameobjects.BlackHole:
                        self.check_object(
                            object)  # gets the slope closest to the light and on the line of light and some other stuff

                    if type(object) == gameobjects.Lens:
                        self.check_lens(object)

                # for lens in lenses:
                #     self.lens_stuff(lens)

                # print(self.current_object_type)
                if type(self.current_object) == gameobjects.Lens:
                    self.ignore_object = self.current_object
                # To do: fix bug causing only one lens to be analyzed

                if self.current_object_type == None:
                    self.border_stuff()
                elif self.current_object_type == 'mirror':
                    self.mirror_stuff()
                elif self.current_object_type == 'glass':
                    self.glass_stuff()

                elif self.current_object_type == 'prism':
                    self.prism_stuff()
                elif self.current_object_type == 'lens':
                    self.lens_stuff(self.current_object)
                elif self.current_object_type == 'blackhole':
                    self.black_hole_stuff()

                self.check_collision_with_other_lights(self.game.objects)

                if self.index >= 1000:
                    self.mini_run = False


    def check_object(self, object):
        # self.linear_function.draw(self.game)

        self.object_counter = 0
        object.get_slopes()

        self.slopes = object.slopes
        # print(slopes)
        i = 0
        for slope in self.slopes:

            if slope == self.slope_before:
                pass
            elif object == self.ignore_object:
                self.ignore_object = None
                if self.in_mirror:
                    self.in_mirror = False
                return
            else:
                if (slope[0][0] - slope[1][0]) == 0:
                    dx = 0.001
                else:
                    dx = (slope[0][0] - slope[1][0])
                # r=math.atan((slope[0][0]-slope[1][0])/dy)

                lf = Linear_Function((slope[0][1] - slope[1][1]) / dx,
                                     self.find_b(((slope[0][1] - slope[1][1]) / dx), slope[0]))
                # lf.draw(self.game)
                x = lf.intercept(self.linear_function)

                y = lf.calculate(x)
                # lf.draw(self.game)
                # self.linear_function.draw(self.game)

                # pygame.draw.circle(self.game.screen,(255,0,0),(x,self.linear_function.calculate(x)),5)
                # # pygame.draw.circle(self.game.screen, (0, 255, 0), slope[0], 5)
                # # pygame.draw.circle(self.game.screen, (0, 255, 0), slope[1], 5)
                # lf.draw(self.game)
                point = (x, self.linear_function.calculate(x))

                if (slope[0][0] - slope[1][0]) == 0:  # checking 'special case slope': |
                    adding = 1
                else:
                    adding = 0
                if x - adding <= max(slope[0][0], slope[1][0]) and x + adding >= min(slope[0][0], slope[1][0]):
                    if y <= max(slope[0][1], slope[1][1]) and y >= min(slope[0][1], slope[1][1]):
                        cases = 0
                        if self.horizontal == 'right':
                            if x >= self.current_starting_point[0]:
                                cases += 1
                                # print('aaaaaaa')
                        else:
                            if x <= self.current_starting_point[0]:
                                cases += 1
                        if self.vertical == 'up':
                            if y <= self.current_starting_point[1]:
                                cases += 1
                        else:
                            if y >= self.current_starting_point[1]:
                                cases += 1
                        # print(self.vertical,self.horizontal,self.r)
                        # print(cases,'aaaaaaaaaaaaaaaaaaaaaa')
                        if cases == 2:
                            # pygame.draw.line(self.game.screen, (0, 255, 0), slope[0], slope[1],
                            #                  5)
                            dist = abs(x - self.current_starting_point[0])
                            if self.current_distance == None:
                                self.object_counter += 1
                                self.current_distance = dist
                                self.current_point = point
                                self.current_slope = slope
                                self.current_object = object

                                if type(object) == gameobjects.Mirror:
                                    self.current_object_type = 'mirror'

                                elif type(object) == gameobjects.ColoredGlass:
                                    self.current_object_type = 'glass'
                                elif type(object) == gameobjects.Lens:
                                    self.current_object_type = 'lens'
                                elif type(object) == gameobjects.Prism:
                                    self.current_object_type = 'prism'
                                elif type(object) == gameobjects.Corridor:
                                    self.current_object_type = 'mirror'
                                elif type(object) == gameobjects.BlackHole:
                                    self.current_object_type = 'blackhole'

                            else:
                                if dist < self.current_distance:
                                    self.current_object = object
                                    self.current_distance = dist
                                    self.current_point = point
                                    self.current_slope = slope
                                    self.object_counter += 1

                                    if type(object) == gameobjects.Mirror:
                                        self.current_object_type = 'mirror'
                                    elif type(object) == gameobjects.ColoredGlass:
                                        self.current_object_type = 'glass'
                                    elif type(object) == gameobjects.Lens:
                                        self.current_object_type = 'lens'
                                    elif type(object) == gameobjects.Prism:

                                        self.current_object_type = 'prism'
                                    elif type(object) == gameobjects.Corridor:
                                        self.current_object_type = 'mirror'
                                    elif type(object) == gameobjects.BlackHole:
                                        self.current_object_type = 'blackhole'

                                        # print('aaa')

        # if self.object_counter>1:
        #     self.ignore_object=object

    def check_lens(self, lens):
        if lens == self.ignore_object:
            self.ignore_object = None
            return
        for index, point in enumerate(lens.lens_points):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                x = point[0]
                y = point[1]
                cases = 0
                if self.horizontal == 'right':
                    if x >= self.current_starting_point[0]:
                        cases += 1
                        # print('aaaaaaa')
                else:
                    if x <= self.current_starting_point[0]:
                        cases += 1
                if self.vertical == 'up':
                    if y <= self.current_starting_point[1]:
                        cases += 1
                else:
                    if y >= self.current_starting_point[1]:
                        cases += 1
                if cases == 2:
                    dist = abs(x - self.current_starting_point[0])
                    if self.current_distance == None:

                        self.current_distance = dist
                        self.current_point = point
                        self.current_slope = None
                        self.current_object = lens
                        self.current_object_type = 'lens'


                    else:
                        if dist < self.current_distance:
                            self.current_distance = dist
                            self.current_point = point
                            self.current_slope = None
                            self.current_object = lens
                            self.current_object_type = 'lens'

        for index, point in enumerate(lens.lens_points2):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                x = point[0]
                y = point[1]
                cases = 0
                if self.horizontal == 'right':
                    if x >= self.current_starting_point[0]:
                        cases += 1
                        # print('aaaaaaa')
                else:
                    if x <= self.current_starting_point[0]:
                        cases += 1
                if self.vertical == 'up':
                    if y <= self.current_starting_point[1]:
                        cases += 1
                else:
                    if y >= self.current_starting_point[1]:
                        cases += 1
                if cases == 2:
                    dist = abs(x - self.current_starting_point[0])
                    if self.current_distance == None:

                        self.current_distance = dist
                        self.current_point = point
                        self.current_slope = None
                        self.current_object = lens
                        self.current_object_type = 'lens'


                    else:
                        if dist < self.current_distance:
                            self.current_distance = dist
                            self.current_point = point
                            self.current_slope = None
                            self.current_object = lens
                            self.current_object_type = 'lens'

    def left_lens(self, lens, direction):
        for index, point in enumerate(lens.lens_points):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                # offset = 0
                # pygame.draw.line(self.game.screen, (255, 255, 80), lens.center1, (point[0] - offset, point[1] - offset))
                slope1 = self.linear_function.a
                slope2 = functions.calculate_slope(point[0], point[1], lens.center1[0], lens.center1[1])
                if slope2 == 'vl':
                    intersect_angle = 90 - math.degrees(math.atan(slope1))
                else:
                    intersect_angle = functions.calculate_intersection_angle(slope1, slope2)
                if direction == 'out':
                    if lens.type == lens.SINGLE_VEX_2 and slope1 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope1)))
                    temp = lens.refraction_index * math.sin(math.radians(intersect_angle))
                    # print(math.degrees(math.asin(temp)))
                    if temp > 1:
                        # print("sdsdsd")
                        temp -= 1
                        ref_angle = math.asin(temp) + math.pi / 2
                    else:
                        ref_angle = math.asin(temp)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(lens.center1[0], lens.center1[1], point[0], point[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_VEX_2:
                        normal_angle = math.pi
                    if index < len(lens.lens_points) / 2:
                        self.r = -normal_angle - ref_angle
                    else:
                        self.r = -normal_angle + ref_angle
                    # print(math.degrees(self.r))
                    self.calibrate_r2()
                if direction == 'in':
                    if lens.type == lens.SINGLE_VEX_2 and slope1 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope1)))
                    ref_angle = math.asin(math.sin(math.radians(intersect_angle)) / lens.refraction_index)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(point[0], point[1], lens.center1[0], lens.center1[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_VEX_2:
                        normal_angle = 0
                    if index < len(lens.lens_points) / 2:
                        self.r = -normal_angle - ref_angle
                    else:
                        self.r = -normal_angle + ref_angle

                # print(math.degrees(self.r))

                self.points.append(point)
                self.colors.append(self.RGB.rgb)
                self.current_starting_point = point
                self.linear_function = Linear_Function(math.tan(-self.r),
                                                       self.find_b(math.tan(-self.r),
                                                                   self.current_starting_point))
                self.calibrate_r2()
                # self.linear_function.draw(self.game)
                break

    def right_lens(self, lens, direction):
        for index, point in enumerate(lens.lens_points2):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                # offset = 0
                # pygame.draw.line(self.game.screen, (255, 255, 80), lens.center2,
                #                  (point[0] - offset, point[1] - offset))
                slope1 = self.linear_function.a
                slope2 = functions.calculate_slope(lens.center2[0], lens.center2[1], point[0], point[1])

                if slope2 == 'vl':
                    intersect_angle = 90 - math.degrees(math.atan(slope1))
                else:
                    intersect_angle = functions.calculate_intersection_angle(slope1, slope2)
                if direction == 'out':
                    if lens.type == lens.SINGLE_VEX and slope1 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope1)))
                    temp = lens.refraction_index * math.sin(math.radians(intersect_angle))
                    # print(math.degrees(math.asin(temp)))
                    if temp > 1:
                        # print("sdsdsd")
                        temp -= 1
                        ref_angle = math.asin(temp) + math.pi / 2
                    else:
                        ref_angle = math.asin(temp)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(lens.center2[0], lens.center2[1], point[0], point[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_VEX:
                        normal_angle = 0

                    if index < len(lens.lens_points2) / 2:
                        self.r = -normal_angle - ref_angle
                    else:
                        self.r = -normal_angle + ref_angle
                    # print(math.degrees(self.r))
                if direction == 'in':
                    if lens.type == lens.SINGLE_VEX and slope1 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope1)))
                    ref_angle = math.asin(math.sin(math.radians(intersect_angle)) / lens.refraction_index)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(point[0], point[1], lens.center2[0], lens.center2[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_VEX:
                        normal_angle = 0
                    if index < len(lens.lens_points2) / 2:
                        self.r = -normal_angle - ref_angle  # + math.pi
                    else:
                        self.r = -normal_angle + ref_angle  # + math.pi

                self.points.append(point)
                self.colors.append(self.RGB.rgb)
                self.current_starting_point = point
                self.linear_function = Linear_Function(math.tan(-self.r),
                                                       self.find_b(math.tan(-self.r),
                                                                   self.current_starting_point))
                self.calibrate_r2()
                # self.linear_function.draw(self.game)
                break

    def left_lens_concave(self, lens, direction):
        for index, point in enumerate(lens.lens_points):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                # offset = 0
                # pygame.draw.line(self.game.screen, (255, 255, 80), lens.center1, (point[0] - offset, point[1] - offset))
                slope1 = self.linear_function.a
                slope2 = functions.calculate_slope(point[0], point[1], lens.center1[0], lens.center1[1])
                if slope2 == 'vl':
                    intersect_angle = 90 - math.degrees(math.atan(slope1))
                else:
                    intersect_angle = functions.calculate_intersection_angle(slope1, slope2)
                if direction == 'in':
                    if lens.type == lens.SINGLE_CAVE_2 and slope2 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope2)))
                    ref_angle = math.asin(math.sin(math.radians(intersect_angle)) / lens.refraction_index)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(point[0], point[1], lens.center1[0], lens.center1[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_CAVE:
                        if index < len(lens.lens_points) / 2:
                            self.r = -normal_angle - ref_angle + math.pi
                        else:
                            self.r = -normal_angle + ref_angle + math.pi
                        # print(math.degrees(ref_angle))
                    elif lens.type == lens.SINGLE_CAVE_2:
                        normal_angle = 0
                        if index < len(lens.lens_points) / 2:
                            self.r = -normal_angle - ref_angle + math.pi
                        else:
                            self.r = -normal_angle + ref_angle + math.pi
                    else:
                        if index < len(lens.lens_points) / 2:
                            self.r = -normal_angle + ref_angle + math.pi
                        else:
                            self.r = -normal_angle - ref_angle + math.pi

                    # print(math.degrees(self.r))
                if direction == 'out':
                    if lens.type == lens.SINGLE_CAVE_2 and slope2 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope2)))
                    temp = lens.refraction_index * math.sin(math.radians(intersect_angle))
                    # print(math.degrees(math.asin(temp)))
                    if temp > 1:
                        temp -= 1
                        ref_angle = math.asin(temp) + math.pi / 2
                    else:
                        ref_angle = math.asin(temp)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(lens.center1[0], lens.center1[1], point[0], point[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_CAVE_2:
                        normal_angle = 0
                        if index < len(lens.lens_points) / 2:
                            self.r = -normal_angle + ref_angle
                        else:
                            self.r = -normal_angle - ref_angle
                    elif lens.type == lens.SINGLE_CAVE:
                        if index < len(lens.lens_points) / 2:
                            self.r = -normal_angle - ref_angle + math.pi
                        else:
                            self.r = -normal_angle + ref_angle + math.pi
                        # print(math.degrees(ref_angle))
                    else:
                        if index < len(lens.lens_points) / 2:
                            self.r = -normal_angle + ref_angle + math.pi
                        else:
                            self.r = -normal_angle - ref_angle + math.pi
                    # print(math.degrees(self.r))

                self.points.append(point)
                self.colors.append(self.RGB.rgb)
                self.current_starting_point = point
                self.linear_function = Linear_Function(math.tan(-self.r),
                                                       self.find_b(math.tan(-self.r),
                                                                   self.current_starting_point))
                self.calibrate_r2()
                # self.linear_function.draw(self.game)
                break

    def right_lens_concave(self, lens, direction):
        for index, point in enumerate(lens.lens_points2):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                # offset = 0
                # pygame.draw.line(self.game.screen, (255, 255, 80), lens.center2,
                #                  (point[0] - offset, point[1] - offset))
                slope1 = self.linear_function.a
                slope2 = functions.calculate_slope(lens.center2[0], lens.center2[1], point[0], point[1])
                if slope2 == 'vl':
                    intersect_angle = 90 - math.degrees(math.atan(slope1))
                else:
                    intersect_angle = functions.calculate_intersection_angle(slope1, slope2)
                if direction == 'in':
                    if lens.type == lens.SINGLE_CAVE and slope2 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope2)))
                    ref_angle = math.asin(math.sin(math.radians(intersect_angle)) / lens.refraction_index)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(point[0], point[1], lens.center2[0], lens.center2[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_CAVE:
                        normal_angle = 0
                        if index < len(lens.lens_points2) / 2:
                            self.r = normal_angle + ref_angle
                        else:
                            self.r = normal_angle - ref_angle
                    else:
                        if index < len(lens.lens_points2) / 2:
                            self.r = -normal_angle - ref_angle + math.pi
                        else:
                            self.r = -normal_angle + ref_angle + math.pi
                if direction == 'out':
                    if lens.type == lens.SINGLE_CAVE and slope2 != 'vl':
                        intersect_angle = abs(math.degrees(math.atan(slope2)))
                    temp = lens.refraction_index * math.sin(math.radians(intersect_angle))
                    # print(math.degrees(math.asin(temp)))
                    if temp > 1:
                        temp -= 1
                        ref_angle = math.asin(temp) + math.pi / 2
                    else:
                        ref_angle = math.asin(temp)
                    # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(lens.center2[0], lens.center2[1], point[0], point[1])
                    # print(math.degrees(normal_angle))
                    if lens.type == lens.SINGLE_CAVE:
                        normal_angle = 0
                    if index < len(lens.lens_points2) / 2:
                        self.r = -normal_angle - ref_angle + math.pi
                    else:
                        self.r = -normal_angle + ref_angle + math.pi
                    # print(math.degrees(self.r))

                self.points.append(point)
                self.colors.append(self.RGB.rgb)
                self.current_starting_point = point
                self.linear_function = Linear_Function(math.tan(-self.r),
                                                       self.find_b(math.tan(-self.r),
                                                                   self.current_starting_point))
                self.calibrate_r2()
                # self.linear_function.draw(self.game)
                break

    def lens_stuff(self, lens):
        lens_collide_point1 = None
        lens_collide_point2 = None
        collides_on_only_one_side = False
        collide_direction = None
        # self.linear_function.draw(self.game)
        for index, point in enumerate(lens.lens_points):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                if lens_collide_point1 is None:
                    lens_collide_point1 = point
        for index, point in enumerate(lens.lens_points2):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                if lens_collide_point2 is None:
                    lens_collide_point2 = point
        last_light_point = self.points[-1]
        starting_lens_side = None
        if lens_collide_point1 is not None:
            dist1 = functions.distance_between_points(last_light_point, lens_collide_point1)
        else:
            starting_lens_side = 2
            collides_on_only_one_side = True
        if lens_collide_point2 is not None:
            dist2 = functions.distance_between_points(last_light_point, lens_collide_point2)
        else:
            starting_lens_side = 1
            collides_on_only_one_side = True

        if collides_on_only_one_side:
            if lens_collide_point1 is None:
                if last_light_point[0] > lens_collide_point2[0]:
                    collide_direction = 'right'
                else:
                    collide_direction = 'left'
            if lens_collide_point2 is None:
                if last_light_point[0] > lens_collide_point1[0]:
                    collide_direction = 'right'
                else:
                    collide_direction = 'left'

        if starting_lens_side is None:
            if dist1 < dist2:
                starting_lens_side = 1
            else:
                starting_lens_side = 2

        if collides_on_only_one_side is False:
            if starting_lens_side == 1:
                if lens.type == lens.CONVEX:
                    self.left_lens(lens, 'in')
                    self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX:
                    self.left_lens(lens, 'in')
                    self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX_2:
                    self.left_lens(lens, 'in')
                    self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_CAVE:
                    self.left_lens_concave(lens, 'in')
                    self.right_lens_concave(lens, 'out')
                if lens.type == lens.SINGLE_CAVE_2:
                    self.left_lens_concave(lens, 'in')
                    self.right_lens_concave(lens, 'out')
                if lens.type == lens.CONCAVE:
                    self.left_lens_concave(lens, 'in')
                    self.right_lens_concave(lens, 'out')
                if lens.type == lens.CAVE_VEX:
                    self.left_lens(lens, 'in')
                    self.right_lens_concave(lens, 'out')
                if lens.type == lens.VEX_CAVE:
                    self.left_lens_concave(lens, 'in')
                    self.right_lens(lens, 'out')
            if starting_lens_side == 2:
                # print("the other side")
                if lens.type == lens.CONVEX:
                    self.right_lens(lens, 'in')
                    self.left_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX:
                    self.right_lens(lens, 'in')
                    self.left_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX_2:
                    self.right_lens(lens, 'in')
                    self.left_lens(lens, 'out')
                if lens.type == lens.SINGLE_CAVE:
                    self.right_lens_concave(lens, 'in')
                    self.left_lens_concave(lens, 'out')
                if lens.type == lens.SINGLE_CAVE_2:
                    self.right_lens_concave(lens, 'in')
                    self.left_lens_concave(lens, 'out')
                if lens.type == lens.CONCAVE:
                    self.right_lens_concave(lens, 'in')
                    self.left_lens_concave(lens, 'out')
                if lens.type == lens.CAVE_VEX:
                    self.right_lens_concave(lens, 'in')
                    self.left_lens(lens, 'out')
                if lens.type == lens.VEX_CAVE:
                    self.right_lens(lens, 'in')
                    self.left_lens_concave(lens, 'out')
        else:
            if starting_lens_side == 1:
                if lens.type == lens.CONVEX:
                    if collide_direction == 'right':
                        self.left_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens(lens, 'in')
                        self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX:
                    if collide_direction == 'right':
                        self.left_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens(lens, 'in')
                        self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX_2:  # still glitchy
                    if collide_direction == 'right':
                        self.left_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens(lens, 'in')
                        self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_CAVE:
                    if collide_direction == 'right':
                        self.left_lens_concave(lens, 'in')
                        self.right_lens_concave(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens_concave(lens, 'out')
                if lens.type == lens.SINGLE_CAVE_2:
                    if collide_direction == 'right':
                        self.left_lens_concave(lens, 'in')
                        self.right_lens_concave(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens_concave(lens, 'out')
                if lens.type == lens.CONCAVE:
                    if collide_direction == 'right':
                        self.left_lens_concave(lens, 'in')
                        self.right_lens_concave(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens_concave(lens, 'out')
                if lens.type == lens.CAVE_VEX:
                    if collide_direction == 'right':
                        self.left_lens(lens, 'in')
                        self.right_lens_concave(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens(lens, 'out')
                if lens.type == lens.VEX_CAVE:
                    if collide_direction == 'right':
                        self.left_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.left_lens(lens, 'in')
                        self.right_lens_concave(lens, 'out')
            if starting_lens_side == 2:
                if lens.type == lens.CONVEX:
                    if collide_direction == 'right':
                        self.right_lens(lens, 'in')
                        self.left_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.right_lens(lens, 'out')
                        # self.left_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX:  # kinda glitchy
                    if collide_direction == 'right':
                        self.right_lens(lens, 'in')
                        self.left_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_VEX_2:  # still glitchy
                    if collide_direction == 'right':
                        self.right_lens(lens, 'in')
                        self.left_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.right_lens(lens, 'out')
                if lens.type == lens.SINGLE_CAVE:
                    if collide_direction == 'left':
                        self.right_lens_concave(lens, 'in')
                        self.left_lens_concave(lens, 'out')
                    if collide_direction == 'right':
                        self.right_lens_concave(lens, 'out')
                if lens.type == lens.SINGLE_CAVE_2:
                    if collide_direction == 'left':
                        self.right_lens_concave(lens, 'in')
                        self.left_lens_concave(lens, 'out')
                    if collide_direction == 'right':
                        self.right_lens_concave(lens, 'out')
                if lens.type == lens.CONCAVE:
                    if collide_direction == 'left':
                        self.right_lens_concave(lens, 'in')
                        self.left_lens_concave(lens, 'out')
                    if collide_direction == 'right':
                        self.right_lens_concave(lens, 'out')
                if lens.type == lens.CAVE_VEX:
                    if collide_direction == 'right':
                        self.right_lens_concave(lens, 'out')
                    if collide_direction == 'left':
                        self.right_lens_concave(lens, 'in')
                        self.left_lens(lens, 'out')
                if lens.type == lens.VEX_CAVE:
                    if collide_direction == 'right':
                        self.right_lens(lens, 'out')
                    if collide_direction == 'left':
                        self.right_lens(lens, 'in')
                        self.left_lens_concave(lens, 'out')

            # else:
        # print("rotated")
        # self.right_lens(lens)
        # if lens.type == lens.CONVEX:
        #     self.left_lens(lens)

    def glass_stuff(self):
        self.points.append(self.current_point)
        self.RGB.compare(
            RGB_Class(self.current_object.color[0], self.current_object.color[1], self.current_object.color[2]))
        transmittance_factor = self.current_object.transmittance
        self.RGB = RGB_Class(int(self.RGB.r * transmittance_factor), int(self.RGB.g * transmittance_factor),
                             int(self.RGB.b * transmittance_factor))
        self.colors.append(self.RGB.rgb)
        # print(self.RGB.rgb)
        self.current_starting_point = self.current_point

        RGB2 = RGB_Class(int(self.RGB.r * (1 - transmittance_factor)), int(self.RGB.g * (1 - transmittance_factor)),
                         int(self.RGB.b * (1 - transmittance_factor)))
        r = self.r
        self.reflect()
        # print(r,self.r)

        self.r = r

    def black_hole_stuff(self):
        self.points.append(self.current_point)
        self.mini_run = False

    def border_stuff(self):

        self.points.append((self.current_point_before[0] + 30000 * math.cos(-self.r),
                            self.current_point_before[1] + 30000 * math.sin(-self.r)))
        self.colors.append(self.RGB.rgb)
        self.mini_run = False

    def reflect(self):

        if (self.current_slope[0][0] - self.current_slope[1][0]) == 0:
            self.slope_angle = math.pi / 2
        else:

            self.slope_angle = math.atan((self.current_slope[0][1] - self.current_slope[1][1]) / (
                    self.current_slope[0][0] - self.current_slope[1][0]))
            if self.current_slope[0][0] >= self.current_slope[1][0] and self.current_slope[0][1] > \
                    self.current_slope[1][1]:
                self.slope_angle = math.pi - self.slope_angle
            elif self.current_slope[1][0] >= self.current_slope[0][0] and self.current_slope[1][1] > \
                    self.current_slope[0][1]:
                self.slope_angle = math.pi - self.slope_angle
            else:
                self.slope_angle = -self.slope_angle
        self.r = 2 * self.slope_angle - self.r
        self.calibrate_r2()

    def make_mirror_light(self, angle, color):
        light1 = Light(self.game, [self.current_point], color, (self.r + angle) * 180 / math.pi,
                       self.light_width)
        light1.current_slope = self.current_slope
        light1.in_mirror = True
        light1.ignore_object = self.current_object
        light1.debug = False

        light1.trace_path2()
        light1.render()

    def callibrate_slope_angle(self):
        if (self.current_slope[0][0] - self.current_slope[1][0]) == 0:
            self.slope_angle = math.pi / 2
        else:

            self.slope_angle = math.atan((self.current_slope[0][1] - self.current_slope[1][1]) / (
                    self.current_slope[0][0] - self.current_slope[1][0]))
            if self.current_slope[0][0] >= self.current_slope[1][0] and self.current_slope[0][1] > \
                    self.current_slope[1][1]:
                self.slope_angle = math.pi - self.slope_angle
            elif self.current_slope[1][0] >= self.current_slope[0][0] and self.current_slope[1][1] > \
                    self.current_slope[0][1]:
                self.slope_angle = math.pi - self.slope_angle
            else:
                self.slope_angle = -self.slope_angle
        self.calibrate_r2()

    def mirror_stuff(self):
        self.counter += 1
        if self.counter > 149:
            self.game.achievements.handle_achievement_unlocked("white mode")
        elif self.counter > 69:
            self.game.achievements.handle_achievement_unlocked("epilepsy")
        # pygame.draw.line(self.game.screen, (0, 0, 255), self.current_slope[0], self.current_slope[1], 5)
        self.points.append(self.current_point)
        reflection_factor = self.current_object.reflection_factor
        transmittance_factor = self.current_object.transmittance

        if not self.in_mirror:
            self.angle = 0
            if transmittance_factor > 0:
                self.make_mirror_light(self.angle, RGB_Class(int(self.RGB.r * transmittance_factor),
                                                             int(self.RGB.g * transmittance_factor),
                                                             int(self.RGB.b * transmittance_factor)).rgb)
        else:
            self.in_mirror = False

        self.RGB = RGB_Class(int(self.RGB.r * reflection_factor), int(self.RGB.g * reflection_factor),
                             int(self.RGB.b * reflection_factor))

        self.colors.append(self.RGB.rgb)

        self.reflect()

        self.current_starting_point = self.current_point

    def prism_stuff(self):
        # pygame.draw.line(self.game.screen, (0, 0, 255), self.current_slope[0], self.current_slope[1], 5)
        self.points.append(self.current_point)
        transmittance = self.current_object.transmittance
        self.RGB = RGB_Class(int(self.RGB.r * transmittance), int(self.RGB.g * transmittance),
                             int(self.RGB.b * transmittance))

        self.colors.append(self.RGB.rgb)

        self.current_starting_point = self.current_point
        self.vector = Vector(math.cos(self.r), -math.sin(self.r))
        # self.vector.draw(self.game.screen,self.current_point)
        self.normalized_vector = self.vector.normalize()
        if not self.in_prism:
            mi = 1 / self.current_object.n
        else:
            mi = self.current_object.n
        self.slope_vector = self.slope_to_vector(self.current_slope)
        # self.slope_vector.draw(self.game.screen,self.current_point)
        if not self.in_prism:
            self.slope_normal_vector = self.slope_vector.normal()
        else:
            self.slope_normal_vector = self.slope_vector.normal().scale(-1)

        # self.slope_normal_vector.draw(self.game.screen,self.current_point)
        try:

            self.new_vector = self.slope_normal_vector.scale(
                math.sqrt(1 - mi ** 2 * (1 - (self.slope_normal_vector.dot(self.normalized_vector)) ** 2))).add(
                self.normalized_vector.substract(
                    self.slope_normal_vector.scale(self.slope_normal_vector.dot(self.normalized_vector))).scale(mi))
            # print('aaaaaaaaaaaaaaaaaaaaaaaaaa')
        except:
            # print('bbbbbbbbbbbbbbbbbbbbbbbbbbb')
            self.new_vector = self.slope_normal_vector.scale(
                math.sqrt(0)).add(
                self.normalized_vector.substract(
                    self.slope_normal_vector.scale(self.slope_normal_vector.dot(self.normalized_vector))).scale(mi))
        # if self.in_prism:
        #     self.new_vector=self.new_vector.substract(self.slope_normal_vector.scale(2*self.new_vector.dot(self.slope_normal_vector)))
        # self.new_vector.draw(self.game.screen,self.current_point)
        self.r = self.new_vector.get_angle()
        self.calibrate_r2()
        self.split_light()

        if self.in_prism == True:
            self.in_prism = False
        else:
            self.in_prism = True

    def slope_to_vector(self, slope):
        return Vector(slope[1][0] - slope[0][0], slope[1][1] - slope[0][1])

    def split_light(self):
        if self.prism_light == False:
            angle = math.pi / 500
            da = angle / 7 * 2
            colors = [(194, 14, 26), (220, 145, 26), (247, 234, 59), (106, 169, 65), (69, 112, 180), (90, 40, 127),
                      (128, 33, 125)]
            red = self.RGB.rgb[0] / 255
            green = self.RGB.rgb[1] / 255
            blue = self.RGB.rgb[2] / 255
            weights = [red, 2 / 3 * red + 1 / 3 * green, 1 / 3 * red + 2 / 3 * green, green,
                       2 / 3 * green + 1 / 3 * blue, 1 / 3 * green + 2 / 3 * blue, blue, 2 / 3 * blue + 1 / 3 * red,
                       1 / 3 * blue + 2 / 3 * red]
            print(self.horizontal)
            if self.horizontal == 'left':
                colors.reverse()
                angle = math.pi / 200
            for x in range(0, 7):
                self.make_prism_light((colors[x][0] * weights[x], colors[x][1] * weights[x], colors[x][2] * weights[x]),
                                      angle)
                angle -= da
            self.mini_run = False

    def make_prism_light(self, color, angle):
        light1 = Light(self.game, [self.current_point], color, (self.r + angle) * 180 / math.pi,
                       self.light_width)
        light1.current_slope = self.current_slope
        light1.in_prism = True
        light1.prism_light = True
        light1.debug = False
        light1.calibrate_r2()
        light1.trace_path2()
        light1.render()

    def calibrate_r2(self):
        if self.r > 2 * math.pi:
            self.r -= 2 * math.pi
        if self.r < 0:
            self.r += 2 * math.pi

    def get_r(self):
        self.r = self.angle / 360 * 2 * math.pi
        if self.r > 2 * math.pi:
            self.r -= 2 * math.pi
        if self.r < 0:
            self.r += 2 * math.pi

    def draw_thick_line(self, surface, x1, y1, x2, y2, color, THICC):
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            for offset in range(THICC):
                try:
                    pygame.gfxdraw.line(surface, x1, y1 + offset, x2, y2 + offset, color)
                except:
                    pass
        else:
            for offset in range(THICC):
                try:
                    pygame.gfxdraw.line(surface, x1 + offset, y1, x2 + offset, y2, color)
                except:
                    pass


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, pos):
        pygame.draw.line(surface, (0, 255, 255), pos, (pos[0] + self.x * 100, pos[1] + self.y * 100))
        pygame.draw.circle(surface, (255, 0, 0), (pos[0] + self.x * 100, pos[1] + self.y * 100), 2)

    def get_angle(self):
        a = -math.atan(self.y / self.x)
        if self.x < 0:
            a += math.pi
        return a

    def normalize(self):
        l = (self.x ** 2 + self.y ** 2) ** (1 / 2)
        return Vector(self.x / l, self.y / l)

    def dot(self, vector):
        return self.x * vector.x + self.y + vector.y

    def scale(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def substract(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y)

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def normal(self):
        return Vector(-self.y, self.x).normalize()


class RGB_Class():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.a = max(r, g, b)
        self.rgb = (r, g, b, self.a)

    def compare(self, RGB2):
        if RGB2.r < self.r:
            self.r = RGB2.r
        if RGB2.g < self.g:
            self.g = RGB2.g
        if RGB2.b < self.b:
            # print('aaa')
            self.b = RGB2.b

        self.update()

    def update(self):
        # print(self.b)
        self.rgb = (self.r, self.g, self.b, self.a)


class Linear_Function:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def calculate(self, number):
        return self.a * number + self.b

    def intercept(self, linear_function):
        if self.a == linear_function.a:
            return -1
        else:
            return (self.b - linear_function.b) / (linear_function.a - self.a)

    def __str__(self):
        return f" {self.a}*x + {self.b}"

    def draw(self, game):
        pygame.draw.line(game.screen, (255, 255, 255), (0, self.calculate(0)),
                         (1000, self.calculate(1000)), 2)
