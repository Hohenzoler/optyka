import pygame
from classes import gameobjects as go

class Bin:
    def __init__(self, game):
        self.game = game
        self.x = self.game.width - 150
        self.y = self.game.height - 200

        self.rect = pygame.Rect(self.x, self.y, 100, 100)

        self.game.objects.append(self)

    def render(self):
        pygame.draw.rect(self.game.screen, 'grey', self.rect)

    def checkCollision(self, obj):
        if obj.rect.colliderect(self.rect) and isinstance(obj, go.GameObject):
            self.game.objects.remove(obj)