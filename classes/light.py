# light.py
import pygame

class Light:
    # Light class for rendering light effects
    def __init__(self, game, points, color, angle, light_width):
        # points is a list that represents endpoints of next lines building a stream of light
        self.points = points
        self.game = game
        self.color = color
        self.angle = angle
        self.light_width = light_width
        self.layer = 0  # Assign a layer value to control rendering order
        self.game.objects.insert(-1, self)

    def render(self):
        # Render the light effect
        try:
            for p in range(0, len(self.points) - 1):
                pygame.draw.line(self.game.screen, self.color, self.points[p], self.points[p + 1], self.light_width)
        except AttributeError:
            pass
