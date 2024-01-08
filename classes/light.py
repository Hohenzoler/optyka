import pygame
import math
from classes import gameobjects, fps
import time


class Light:
    def __init__(self, game, points, color, angle, light_width):
        # points is a list that represents endpoints of next lines building a stream of light
        self.points = points
        self.game = game
        self.color = color
        self.angle = angle
        self.light_width = light_width
        self.layer = 0  # Assign a layer value to control rendering order
        self.game.objects.insert(-1, self)
        self.points=(self.points)

        self.x=self.points[0][0]
        self.y=self.points[0][1]
        self.count=1

    def render(self):
        try:
            for p in range(0, len(self.points) - 1):
                pygame.draw.line(self.game.screen, self.color, self.points[p], self.points[p + 1], self.light_width)
        except AttributeError:  # if line doesnt have evailible points
            pass
    def callibrate_r(self):
        if self.r > 2*math.pi:
            self.r-=2*math.pi
    def trace_path(self, max_time_seconds=(1/fps.return_fps())):
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
                            self.trace=False
                            # object_angle=-object.angle/360*2*math.pi
                            # print(object_angle)
                            # self.bend(object_angle)
            if type(object) == gameobjects.Mirror:
                if self.vp_rect.colliderect(object.rect):
                    # print('touch')
                    self.points.append((self.vx, self.vy))

                    # object_angle = -object.angle / 360 * 2 * math.pi
                    # print(object_angle)
                    angle=self.find_angle(object)
                    # print(self.r)
                    self.bend(angle)

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
    def dist(self,x1,y1,x2,y2):
        return ((x1-x2)**2 + (y1-y2)**2)**(1/2)
    def update_vp(self):

        self.vp = (self.vx, self.vy)  # vp - virtual pointer - a place where the light will come
        self.vp_rect=pygame.Rect(self.vx,self.vy,1,1)
    def forward(self):
        self.vx+=math.cos(self.r)
        self.vy+=math.sin(self.r)

        # print(self.vx,self.vy)