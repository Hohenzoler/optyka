import math
from settingsSetup import *
import pygame as pg
HALF_FOV = settings['Flashlight_FOV'] // 2
NUM_RAYS = settings['Flashlight_Rays']
MAX_DEPTH = settings['Flashlight_Depth']


def collidepoly(poly1, poly2):
    def is_point_inside_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    for point in poly1:
        if is_point_inside_polygon(point, poly2):
            return True

    for point in poly2:
        if is_point_inside_polygon(point, poly1):
            return True

    return False

def ray_cast(game_obj, flashlight):
    ox, oy = flashlight.points[0]

    ray_angle = flashlight.angle - HALF_FOV + 0.0001
    for ray in range(NUM_RAYS):
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        depth = MAX_DEPTH

        # remove fishbowl effect
        depth *= math.cos(flashlight.angle - ray_angle)

        pg.draw.line(game_obj.screen, (255, 255, 255), (100 * ox, 100*oy), (100*ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)