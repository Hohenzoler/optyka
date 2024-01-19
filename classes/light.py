import pygame
import math
from classes import gameobjects, fps
import time
import functions


class Light:
    def __init__(self, game, points, color, angle, light_width):
        # points is a list that represents endpoints of next lines building a stream of light
        self.starting_point=points[0]
        self.points = points
        self.game = game
        self.color = color
        self.angle = angle
        self.light_width = light_width
        self.layer = 0  # Assign a layer value to control rendering order
        self.game.objects.insert(-1, self)
        self.colors=[]
        self.RGB = RGB(self.color[0], self.color[1], self.color[2])
        self.colors.append(self.RGB.rgb)
        self.x=self.points[0][0]
        self.y=self.points[0][1]
        self.count=1

    def render(self):
        try:
            pygame.draw.lines(self.game.screen, self.color, False, self.points, self.light_width)
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
                        # print('touch')
                        self.points.append((self.vx, self.vy))
                        # self.RGB.compare(RGB(255,255,0)) - enter to code to try for yourself!!! :)
                        self.colors.append(self.RGB.rgb)

                        # object_angle = -object.angle / 360 * 2 * math.pi
                        # print(object_angle)
                        angle=self.find_angle2(object)

                        # print(self.r)
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
        # print(len(triangles))
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
            print(sum,area)
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
