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
        self.debug=False
        self.prism_light=False
        self.in_prism=False
        self.in_mirror=False
        self.main_light_slope=None
        self.linear_function = None
        self.starting_point=points[0]
        self.points = points
        self.game = game
        self.color = color
        self.angle = angle
        self.light_width = light_width
        self.layer = 0  # Assign a layer value to control rendering order
        #self.game.objects.insert(-1, self)
        self.colors=[]
        self.RGB = RGB_Class(self.color[0], self.color[1], self.color[2])
        self.colors.append(self.RGB.rgb)
        self.x=self.points[0][0]
        self.y=self.points[0][1]
        self.count=1
        self.get_r()
        self.alpha = alpha
        self.ignore_object = None
        self.counter = 0

        # print(self.r,self.linear_function)
    def find_b(self,a,point):
        return point[1]-a*point[0]

    def render(self):
        try:
            ### For RTX Flashlight ###
            if self.game.settings['HD_Flashlight'] == 'ON':
                #### Original ####
                # new_line_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
                # new_line_surface.set_alpha(self.alpha)
                for x in range(0, len(self.points) - 1):
                    #### Beta testing stuff ####
                    current_ray = Ray(self.points[x], self.points[x+1], self.colors[x])
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
                            if functions.do_lines_intersect(ray.start_point, ray.end_point, current_ray.start_point, current_ray.end_point):
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

        except (AttributeError, ValueError):
            pass
    #NON - RECURSIVE

    def special_case_adjust(self):
        if self.r==math.pi/2:
            self.r=math.pi/2+0.00001
        elif self.r==3*math.pi/2:
            self.r=3*math.pi/2+0.00001
        elif self.r==0:
            self.r=0.00001
        elif self.r==math.pi:
            self.r=math.pi+0.00001
    def trace_path2(self):
        self.current_starting_point = self.starting_point
        self.special_case_adjust()
        self.mini_run=True
        self.index=0
        while self.mini_run:
            if self.r < math.pi:
                self.vertical = 'up'
            else:
                self.vertical = 'down'
            if self.r < 3 / 2 * math.pi and self.r > 1 / 2 * math.pi:
                self.horizontal = 'left'
            else:
                self.horizontal = 'right'
            self.index+=1
            self.linear_function = Linear_Function(math.tan(-self.r),
                                                   self.find_b(math.tan(-self.r), self.current_starting_point))
            if self.debug==True:
                self.linear_function.draw(self.game)
            try:
                self.slope_before=self.current_slope
            except:
                self.slope_before=self.main_light_slope
            self.current_point_before=self.current_starting_point
            self.current_distance = None
            self.current_point = None
            self.current_slope = None
            self.current_object=None
            lenses = []
            for object in self.game.objects:
                if type(object) == gameobjects.Mirror or type(object)==gameobjects.ColoredGlass or type(object)==gameobjects.Prism:
                    self.check_object(object) # gets the slope closest to the light and on the line of light and some other stuff
                if type(object) == gameobjects.Lens:
                    self.check_object(object)

            # To do: fix bug causing only one lens to be analyzed

            if self.current_slope == None:
                self.border_stuff()
            elif self.current_object_type=='mirror':
                self.mirror_stuff()
            elif self.current_object_type=='glass':
                self.glass_stuff()
            elif self.current_object_type=='lens':
                self.lens_stuff(self.current_object)
            elif self.current_object_type=='prism':
                self.prism_stuff()



            if self.index >= 100:
                self.mini_run = False
    def check_object(self,object):


        self.object_counter=0
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
                    self.in_mirror=False
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
                #
                # pygame.draw.circle(self.game.screen,(255,0,0),(x,self.linear_function.calculate(x)),5)
                # # pygame.draw.circle(self.game.screen, (0, 255, 0), slope[0], 5)
                # # pygame.draw.circle(self.game.screen, (0, 255, 0), slope[1], 5)
                # lf.draw(self.game)
                point = (x, self.linear_function.calculate(x))
                if x <= max(slope[0][0], slope[1][0]) + 1 and x >= min(slope[0][0], slope[1][0]) - 1:
                    if y <= max(slope[0][1], slope[1][1]) + 1 and y >= min(slope[0][1], slope[1][1]) - 1:
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
                        # print(cases)
                        if cases == 2:
                            pygame.draw.line(self.game.screen, (0, 255, 0), slope[0], slope[1],
                                             5)
                            dist = abs(x - self.current_starting_point[0])
                            if self.current_distance == None:
                                self.object_counter+=1
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
        # if self.object_counter>1:
        #     self.ignore_object=object

    def left_lens(self, lens):
        for index, point in enumerate(lens.lens_points):
            if functions.is_linear_function_passing_through_point(self.linear_function, point):
                offset = 0
                pygame.draw.line(self.game.screen, (255, 255, 80), lens.center1, (point[0] - offset, point[1] - offset))
                slope1 = self.linear_function.a
                slope2 = functions.calculate_slope(point[0], point[1], lens.center1[0], lens.center1[1])
                intersect_angle = int(functions.calculate_intersection_angle(slope1, slope2))
                ref_angle = math.asin(math.sin(math.radians(intersect_angle)) / lens.refraction_index)
                # print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                normal_angle = functions.calculate_angle(point[0], point[1], lens.center1[0], lens.center1[1])
                # print(math.degrees(normal_angle))
                if index < len(lens.lens_points) / 2:
                    self.r = -normal_angle - ref_angle
                else:
                    self.r = -normal_angle + ref_angle

                # print(math.degrees(self.r))

                self.points.append(point)
                self.colors.append(self.RGB.rgb)
                self.current_starting_point = self.current_point #point
                self.linear_function = Linear_Function(math.tan(-self.r),
                                                       self.find_b(math.tan(-self.r),
                                                                   self.current_starting_point))
                self.linear_function.draw(self.game)
                break
    def right_lens(self, lens):
        try:
            for index, point in enumerate(lens.lens_points2):
                if functions.is_linear_function_passing_through_point(self.linear_function, point):
                    offset = 0
                    pygame.draw.line(self.game.screen, (255, 255, 80), lens.center2,
                                     (point[0] - offset, point[1] - offset))
                    slope1 = self.linear_function.a
                    slope2 = functions.calculate_slope(lens.center2[0], lens.center2[1], point[0], point[1])
                    intersect_angle = int(functions.calculate_intersection_angle(slope2, slope1))
                    temp = lens.refraction_index * math.sin(math.radians(intersect_angle))
                    if temp > 1:
                        temp -= 1
                    ref_angle = math.asin(temp)
                    print(str(intersect_angle) + " | " + str(math.degrees(ref_angle)))
                    normal_angle = functions.calculate_angle(lens.center2[0], lens.center2[1], point[0], point[1])
                    print(math.degrees(normal_angle))
                    if index < len(lens.lens_points2) / 2:
                        self.r = -normal_angle - ref_angle
                    else:
                        self.r = -normal_angle + ref_angle
                    print(math.degrees(self.r))

                    self.points.append(point)
                    self.colors.append(self.RGB.rgb)
                    self.current_starting_point = self.current_point #point
                    self.linear_function = Linear_Function(math.tan(-self.r),
                                                           self.find_b(math.tan(-self.r),
                                                                       self.current_starting_point))
                    self.linear_function.draw(self.game)
                    break
        except:
            pass
    def lens_stuff(self, lens):
            if abs(self.angle) not in range(int(abs(lens.angle) + 90), int(abs(lens.angle) + 270)): # light shining from left to right # unfinished, bug when rotating >180deg
                #print(abs(lens.angle))
                self.left_lens(lens)
                if lens.type == lens.CONVEX:
                    self.right_lens(lens)

            else:
                print("rotated")
                self.right_lens(lens)
                if lens.type == lens.CONVEX:
                    self.left_lens(lens)
            self.current_starting_point = self.current_point
            self.calibrate_r2()



    def glass_stuff(self):
        self.points.append(self.current_point)
        self.RGB.compare(RGB_Class(self.current_object.color[0],self.current_object.color[1],self.current_object.color[2]))
        transmittance_factor = self.current_object.transmittance
        self.RGB = RGB_Class(int(self.RGB.r * transmittance_factor), int(self.RGB.g * transmittance_factor),
                       int(self.RGB.b * transmittance_factor))
        self.colors.append(self.RGB.rgb)
        #print(self.RGB.rgb)
        self.current_starting_point = self.current_point

        RGB2=RGB_Class(int(self.RGB.r * (1-transmittance_factor)), int(self.RGB.g * (1-transmittance_factor)),
                       int(self.RGB.b * (1-transmittance_factor)))
        r=self.r
        self.reflect()
        print(r,self.r)


        self.r=r

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
    def mirror_stuff(self):
        self.counter += 1
        if self.counter > 99:
            self.game.achievements.handle_achievement_unlocked("back and forth 2.0")
        elif self.counter > 49:
            self.game.achievements.handle_achievement_unlocked("back and forth")
        pygame.draw.line(self.game.screen, (0, 0, 255), self.current_slope[0], self.current_slope[1], 5)
        self.points.append(self.current_point)
        reflection_factor = self.current_object.reflection_factor
        transmittance_factor = self.current_object.transmittance

        if not self.in_mirror:
            self.angle = 0
            self.make_mirror_light(self.angle, RGB_Class(int(self.RGB.r  * transmittance_factor), int(self.RGB.g * transmittance_factor),
                       int(self.RGB.b * transmittance_factor)).rgb)
        else:
            self.in_mirror=False

        self.RGB = RGB_Class(int(self.RGB.r * reflection_factor), int(self.RGB.g * reflection_factor),
                             int(self.RGB.b * reflection_factor))

        self.colors.append(self.RGB.rgb)

        self.reflect()


        self.current_starting_point = self.current_point
    def first_difract(self,prism):
        n=prism.n
        fi=prism.fi
        self.r=fi/2+self.r+(round(prism.angle))/180*math.pi-math.asin(math.sin((fi/2+self.r))/n)

    def second_difract(self,prism):
        n = prism.n
        fi = prism.fi
        self.r=math.pi-math.asin(math.sin(1/2*prism.angle+fi-self.r)/n)
    def prism_stuff(self):

        pygame.draw.line(self.game.screen, (0, 0, 255), self.current_slope[0], self.current_slope[1], 5)
        self.points.append(self.current_point)
        transmittance = self.current_object.transmittance
        self.RGB = RGB_Class(int(self.RGB.r * transmittance), int(self.RGB.g * transmittance),
                             int(self.RGB.b * transmittance))

        self.colors.append(self.RGB.rgb)
        if self.in_prism:
            self.first_difract(self.current_object)
        else:
            self.first_difract(self.current_object)

        if not self.in_prism and self.prism_light==False:
            angle=math.pi/18
            da=math.pi/63
            colors=[(194, 14, 26),(220, 145, 26),(247, 234, 59),(106, 169, 65),(69, 112, 180),(90, 40, 127),(128, 33, 125)]
            red=self.RGB.rgb[0]/255
            green=self.RGB.rgb[1]/255
            blue=self.RGB.rgb[2] / 255
            weights=[red,2/3*red+1/3*green,1/3*red+2/3*green,green,2/3*green+1/3*blue,1/3*green+2/3*blue,blue,2/3*blue+1/3*red,1/3*blue+2/3*red]
            for x in range(0,7):
                self.make_prism_light((colors[x][0]*weights[x],colors[x][1]*weights[x],colors[x][2]*weights[x]),angle)
                angle-=da
            self.mini_run = False


        self.current_starting_point = self.current_point
        if self.in_prism==True:
            self.in_prism=False
        else:
            self.in_prism=True

    def make_mirror_light(self, angle, color):
        light1 = Light(self.game, [self.current_point], color, (self.r + angle) * 180 / math.pi,
                       self.light_width)
        light1.current_slope = self.current_slope
        light1.in_mirror = True
        light1.ignore_object = self.current_object
        light1.debug = False
        light1.trace_path2()
        light1.render()

    def make_prism_light(self,color,angle):
        light1 = Light(self.game, [self.current_point], color, (self.r + angle) * 180 / math.pi,
                         self.light_width)
        light1.current_slope = self.current_slope
        light1.in_prism = True
        light1.prism_light=True
        light1.debug=False
        light1.trace_path2()
        light1.render()




    def calibrate_r2(self):
        if self.r>2*math.pi:
            self.r-=2*math.pi
        if self.r<0:
            self.r+=2*math.pi

    def get_r(self):
        self.r=self.angle/360*2*math.pi
        if self.r>2*math.pi:
            self.r-=2*math.pi
        if self.r<0:
            self.r+=2*math.pi

    def draw_thick_line(self, surface, x1, y1, x2, y2, color, THICC):
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            for offset in range(THICC):
                pygame.gfxdraw.line(surface, x1, y1 + offset, x2, y2 + offset, color)
        else:
            for offset in range(THICC):
                pygame.gfxdraw.line(surface, x1 + offset, y1, x2 + offset, y2, color)





    def callibrate_r(self):
        if self.r > 2*math.pi:
            self.r-=2*math.pi
    def trace_path(self, max_time_seconds=(1/fps.return_fps())):
        self.points=[self.starting_point]

        self.colors = []
        self.RGB = RGB(self.color[0], self.color[1], self.color[2])
        self.colors.append(self.RGB.rgb)
        self.r=-self.angle/360*2*math.pi

        self.vx = self.x
        self.vy = self.y
        self.trace=True
        start_time = time.time()
        while self.trace and (time.time() - start_time) < max_time_seconds:
            # print(self.r)
            self.callibrate_r()
            self.forward()
            self.update_vp()
            self.border()
            self.collision_check()
    def border(self):
        if self.vx<0 or self.vx>self.game.width or self.vy<0 or self.vy>self.game.height:
            self.points.append((self.vx, self.vy))
            self.trace=False
    def bend(self,angle):
        # self.r=2*math.pi-(math.pi+self.r-2*angle)
        self.r = 2*angle-self.r+math.pi

    def area(self,triangle):
        p1,p2,p3=triangle

        a=self.length(p1,p2)
        b = self.length(p3, p2)
        c = self.length(p1, p3)
        s=(a+b+c)/2
        return (s*(s-a)*(s-b)*(s-c))**(1/2)
    def length(self,p1,p2):
        return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1/2)
    def find_angle2(self,object):
        triangles=object.get_triangles()
        i=0
        for triangle in triangles:

            area=self.area(triangle)
            t1=(triangle[0],triangle[1],self.vp)
            area1=self.area(t1)

            t2 = (triangle[2], triangle[1], self.vp)
            area2 = self.area(t2)

            t3 = (triangle[0], triangle[2], self.vp)
            area3 = self.area(t3)

            sum=area1+area2+area3
            if sum<=area+200:
                pygame.draw.polygon(self.game.screen, (255, 255, 255), triangle)
                # print(math.asin((triangle[1][0]-triangle[2][0])/self.length(triangle[1],triangle[2])))
                return math.asin((triangle[1][0]-triangle[2][0])/self.length(triangle[1],triangle[2]))

            i+=1
        return self.find_angle(object)

    def find_angle(self,object):
        two_points=[]
        two_points_distance=[]
        for point in object.points:
            if len(two_points)<2:
                two_points.append(point)
                two_points_distance.append(self.dist(self.vx,self.vy,point[0],point[1]))
            else:
                distance = self.dist(self.vx,self.vy,point[0],point[1])
                if distance< two_points_distance[0]:
                    two_points[0]=point
                    two_points_distance[0]=distance
                elif distance< two_points_distance[1]:
                    two_points[1]=point
                    two_points_distance[1]=distance

        angle=math.asin((two_points[0][1] - two_points[1][1]) / self.dist(two_points[0][0], two_points[0][1], two_points[1][0],two_points[1][1]))
        return angle
    def two_points_angle(self,two_points):
        return math.asin(
            (two_points[0][1] - two_points[1][1]) / self.dist(two_points[0][0], two_points[0][1], two_points[1][0],
                                                              two_points[1][1]))
    def dist(self,x1,y1,x2,y2):
        return ((x1-x2)**2 + (y1-y2)**2)**(1/2)
    def update_vp(self):

        self.vp = (self.vx, self.vy)  # vp - virtual pointer - a place where the light will come
        self.vp_rect=pygame.Rect(self.vx, self.vy, 1, 1)
        self.vp_polygon = [(self.vx, self.vy + 1), (self.vx + 1, self.vy+1), (self.vx + 1, self.vy), (self.vx, self.vy)]
        #pygame.draw.polygon(self.game.screen, self.color, self.vp_polygon) # For visualizing hitbox
    def forward(self):

        is_mirror = False

        for object in self.game.objects:
            if type(object)==gameobjects.Mirror:
                is_mirror = True
        if is_mirror == False:
            self.vx += 1000 * math.cos(self.r)
            self.vy += 1000 * math.sin(self.r)
        else:
            self.vx += math.cos(self.r)
            self.vy += math.sin(self.r)


        # print(self.vx,self.vy)


class RGB_Class():
    def __init__(self,r,g,b):
        self.r=r
        self.g=g
        self.b=b
        self.a = max(r, g, b)
        self.rgb=(r,g,b, self.a)
    def compare(self,RGB2):
        if RGB2.r<self.r:
            self.r=RGB2.r
        if RGB2.g < self.g:
            self.g = RGB2.g
        if RGB2.b<self.b:
            # print('aaa')
            self.b=RGB2.b

        self.update()

    def update(self):
        # print(self.b)
        self.rgb=(self.r,self.g,self.b, self.a)
class Linear_Function:
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def calculate(self,number):
        return self.a*number+self.b
    def intercept(self,linear_function):
        if self.a==linear_function.a:
            return -1
        else:
            return (self.b-linear_function.b)/(linear_function.a-self.a)
    def __str__(self):
        return f" {self.a}*x + {self.b}"
    def draw(self,game):
        pygame.draw.line(game.screen, (255, 255, 255), (0, self.calculate(0)),
                         (1000, self.calculate(1000)), 2)


