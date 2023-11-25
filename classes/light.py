import pygame


class Light:
    def __init__(self, game, points, color, angle, width):
        # points is a list that represents endpoints of next lines building a stream of light
        self.points = points
        self.game = game
        self.color = color
        self.angle = angle
        self.width = width
        self.game.objects.insert(-1, self)



    def render(self):
        for p in range(0, len(self.points) - 1):
            pygame.draw.line(self.game.screen, self.color, self.points[p], self.points[p + 1], self.width)
