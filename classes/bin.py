import pygame
from classes import gameobjects as go
from classes import sounds

class Bin:
    def __init__(self, game):
        self.game = game
        self.x = self.game.width - 200
        self.y = self.game.height - 70
        self.layer = 10
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

        self.game.objects.append(self)

        self.bin_img = pygame.image.load("images/trash1.png")

    def render(self):
        self.game.screen.blit(self.bin_img, self.rect)

    def checkCollision(self, obj):
        if obj.rect.colliderect(self.rect) and isinstance(obj, go.GameObject):
            self.game.objects.remove(obj)
            sounds.destroy_sound()