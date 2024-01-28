import pygame
from classes import gameobjects as go
from classes import sounds, parkinson as particles, achievements
import random

class Bin:
    def __init__(self, game):
        self.particle_system = particles.UnityParticleSystem()
        self.game = game
        self.x = self.game.width - 150
        self.y = self.game.height - 200

        self.rect = pygame.Rect(self.x, self.y, 100, 100)

        self.particle_center_x = self.x + 88
        self.particle_center_y = self.y + 60

        self.game.objects.append(self)

        self.bin_img = pygame.image.load("images/trash1.png")

        self.load_parameters()

        self.game.objects.append(self)

        self.achievements = game.achievements

    def checkCollision(self, obj):
        if obj.rect.colliderect(self.rect) and isinstance(obj, go.GameObject):
            self.game.objects.remove(obj)
            sounds.destroy_sound()
            achievements.Achievements.handle_achievement_unlocked(self.achievements, "BIN")
            for i in range(random.randint(60, 300)):
                self.particle_system.add_particle(self.particle_center_x, self.particle_center_y, random.uniform(-2, 2), random.uniform(-2, 2), 1000, random.randint(1, 7), random.randint(130, 255), random.randint(0, 130), 0, 200)

    def render(self):
        self.game.screen.blit(self.bin_img, self.rect)
        self.particle_system.update()
        self.particle_system.draw(self.game.screen)

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

        self.particle_center_x = self.x + self.rect_w//2
        self.particle_center_y = self.y + self.rect_h//2


