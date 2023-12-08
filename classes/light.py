import pygame
import math
from classes import gameobjects

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
    def trace_path(self):
        self.r=2*math.pi-self.angle/360*2*math.pi
        print(self.r)
        self.vx = self.x
        self.vy = self.y
        self.trace=True
        while self.trace:
            self.forward()
            self.update_vp()
            self.border()
            self.collision_check()
    def border(self):
        if self.vx<0 or self.vx>self.game.width or self.vy<0 or self.vy>self.game.height:
            self.points.append((self.vx, self.vy))
            self.trace=False
            print('b')
    def bend(self,angle):
        # self.r=2*math.pi-(math.pi+self.r-2*angle)
        self.r = -(math.pi + self.r - 2 * angle)
    def collision_check(self):
        for object in self.game.objects:
            if type(object)==gameobjects.Flashlight or type(object) == gameobjects.Mirror:
                if self.vp_rect.colliderect(object.rect):
                    if self.count == 1:
                        self.flashlight = object
                        self.count = 0
                    elif object == self.flashlight:
                        pass
                    else:
                        if self.vp_rect.colliderect(object.rect):
                            print('a')
                            self.points.append((self.vx, self.vy))
                            object_angle=-object.angle/360*2*math.pi
                            print(object_angle)
                            self.bend(object_angle)
    def update_vp(self):

        self.vp = (self.vx, self.vy)  # vp - virtual pointer - a place where the light will come
        self.vp_rect=pygame.Rect(self.vx,self.vy,1,1)
    def forward(self):
        self.vx+=math.cos(self.r)
        self.vy+=math.sin(self.r)

        # print(self.vx,self.vy)