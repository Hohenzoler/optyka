import pygame
import math
from classes import gameobjects, fps
import time
import functions
import settingsSetup
class Light:
    def __init__(self, game, points, color, angle, light_width, alpha=255):
        # points is a list that represents endpoints of next lines building a stream of light
        self.starting_point=points[0]
        self.points = points
        self.game = game
        self.color = color
        self.angle = angle
        self.light_width = light_width
        self.layer = 0  # Assign a layer value to control rendering order
        #self.game.objects.insert(-1, self)
        self.colors=[]
        self.RGB = RGB(self.color[0], self.color[1], self.color[2])
        self.colors.append(self.RGB.rgb)
        self.x=self.points[0][0]
        self.y=self.points[0][1]
        self.count=1
        self.get_r()
        self.alpha = alpha

        # print(self.r,self.linear_function)
    def find_b(self,a,point):
        return point[1]-a*point[0]

    def trace_path2(self):
        self.current_starting_point = self.starting_point

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
            #self.linear_function.draw(self.game)
            try:
                self.slope_before=self.current_slope
            except:
                self.slope_before=None
            self.current_point_before=self.current_starting_point
            self.current_distance = None
            self.current_point = None
            self.current_slope = None
            self.current_object=None

            for object in self.game.objects:
                if type(object) == gameobjects.Mirror or type(object)==gameobjects.ColoredGlass:
                    self.check_object(object) # gets the slope closest to the light and on the line of light and some other stuff



            if self.current_slope == None:
                self.border_stuff()
            elif self.current_object_type=='mirror':
                self.mirror_stuff()
            elif self.current_object_type=='glass':
                self.glass_stuff()

            if self.index >= 10:
                self.mini_run = False
    def check_object(self,object):


        object.get_slopes()
        self.slopes = object.slopes
        # print(slopes)
        i = 0
        for slope in self.slopes:
            if slope == self.slope_before:
                pass
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
                # if i%2==0:
                #     pygame.draw.circle(self.game.screen,(255,0,0),(x,self.linear_function.calculate(x)),2)
                #     pygame.draw.circle(self.game.screen, (0, 255, 0), slope[0], 2)
                #     pygame.draw.circle(self.game.screen, (0, 255, 0), slope[1], 2)
                #     lf.draw(self.game)
                # print(slope[0][0],slope[1][0],x)
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
                                self.current_distance = dist
                                self.current_point = point
                                self.current_slope = slope
                                self.current_object = object
                                if type(object) == gameobjects.Mirror:
                                    self.current_object_type = 'mirror'

                                elif type(object) == gameobjects.ColoredGlass:
                                    self.current_object_type = 'glass'

                            else:
                                if dist < self.current_distance:
                                    self.current_object = object
                                    self.current_distance = dist
                                    self.current_point = point
                                    self.current_slope = slope
                                    if type(object) == gameobjects.Mirror:
                                        self.current_object_type = 'mirror'
                                    elif type(object) == gameobjects.ColoredGlass:
                                        self.current_object_type = 'glass'

    def glass_stuff(self):
        self.points.append(self.current_point)
        self.RGB.compare(RGB(self.current_object.color[0],self.current_object.color[1],self.current_object.color[2]))
        self.colors.append(self.RGB.rgb)
        #print(self.RGB.rgb)
        self.current_starting_point = self.current_point
    def border_stuff(self):
        self.points.append((self.current_point_before[0] + 1000 * math.cos(-self.r),
                            self.current_point_before[1] + 1000 * math.sin(-self.r)))
        self.colors.append(self.RGB.rgb)
        self.mini_run = False
    def mirror_stuff(self):
        pygame.draw.line(self.game.screen, (0, 0, 255), self.current_slope[0], self.current_slope[1], 5)
        self.points.append(self.current_point)
        self.colors.append(self.RGB.rgb)
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

        self.current_starting_point = self.current_point
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

    def render(self):
        try:
            ### For RTX Flashlight ###
            if self.game.settings['HD_Flashlight'] == 'ON':
                new_line_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
                new_line_surface.set_alpha(self.alpha)
                for x in range(0,len(self.points)-1):
                    pygame.draw.line(new_line_surface, self.colors[x],self.points[x],self.points[x+1],self.light_width)
                self.game.screen.blit(new_line_surface, (0, 0))
            ### For Simple Flashlight ###
            else:
                for x in range(0,len(self.points)-1):
                    pygame.draw.line(self.game.screen, self.colors[x],self.points[x],self.points[x+1],self.light_width)

            # pygame.draw.lines(surface, [200, 0, 0, self.alpha], False, self.points, self.light_width)

        except (AttributeError, ValueError):
            pass









































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
    def collision_check(self):

        for object in self.game.objects:
            if type(object)==gameobjects.Flashlight:
                if self.vp_rect.colliderect(object):
                    if self.count == 1:
                        self.flashlight = object
                        self.count = 0
                    elif object == self.flashlight:
                        pass
                    else:
                        if self.vp_rect.colliderect(object.rect):
                            # print('touch')
                            self.points.append((self.vx, self.vy))
                            self.colors.append(self.RGB.rgb)
                            self.trace=False
                            # object_angle=-object.angle/360*2*math.pi
                            # print(object_angle)
                            # self.bend(object_angle)
            if type(object) == gameobjects.Mirror:
                if self.vp_rect.colliderect(object.rect):
                    if functions.collidepoly(self.vp_polygon, object.points): # Changed colliderect to collidepoly for optimal hitboxes
                        # ('touch')
                        self.points.append((self.vx, self.vy))
                        # self.RGB.compare(RGB(255,255,0)) - enter to code to try for yourself!!! :)
                        self.colors.append(self.RGB.rgb)

                        # object_angle = -object.angle / 360 * 2 * math.pi
                        # (object_angle)
                        angle=self.find_angle2(object)

                        self.bend(angle)
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


class RGB():
    def __init__(self,r,g,b):
        self.r=r
        self.g=g
        self.b=b
        self.rgb=(r,g,b)
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
        self.rgb=(self.r,self.g,self.b)
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


