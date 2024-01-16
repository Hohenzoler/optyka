import pygame
from classes import gameobjects as go
from classes import sounds, images

class Bin:
    def __init__(self, game):
        self.game = game
        self.x = self.game.width - 150
        self.y = self.game.height - 200

        self.rect = pygame.Rect(self.x, self.y, 100, 100)

        self.game.objects.append(self)

        self.bin_img = images.bin

        self.load_parameters()

        self.game.objects.append(self)

    def render(self):
        self.game.screen.blit(self.bin_img, self.rect)

    def checkCollision(self, obj):
        if obj.rect.colliderect(self.rect) and isinstance(obj, go.GameObject):
            self.game.objects.remove(obj)
            sounds.destroy_sound()

    def load_settings(self):
        self.load_parameters()

    def load_parameters(self):
        settings = self.game.settings

        self.x = self.game.width - self.game.width // 10
        self.y = self.game.height - self.game.height // 4

        if settings['HOTBAR_POSITION'] != 'bottom':
            self.y = self.game.height - self.game.height // 7
            if settings['HOTBAR_POSITION'] != 'right':
                self.x = self.game.width - self.game.width // 10

            else:
                self.x = self.game.width - self.game.width // 5


        self.rect_w = self.game.width // 14
        self.rect_h = self.game.height // 8

        self.bin_img = pygame.transform.scale(self.bin_img, (self.rect_w, self.rect_h))

        self.rect = pygame.Rect(self.x, self.y, self.rect_w, self.rect_h)


