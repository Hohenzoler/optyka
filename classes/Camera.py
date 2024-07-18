import pygame
from classes import gameobjects
from classes import parkinson
import random

class Camera:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.particle_system = parkinson.UnityParticleSystem()


    def update(self):
        self.particle_system.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.add_movement_particles()

        if keys[pygame.K_RIGHT]:  # Right arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0] - 10, self.game.points[i][1])

            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x - 10, obj.rect.y, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0] - 10, obj.points[i][1])
            self.x -= 10

        if keys[pygame.K_LEFT]:  # Left arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0] + 10, self.game.points[i][1])

            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x + 10, obj.rect.y, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0] + 10, obj.points[i][1])
            self.x += 10

        if keys[pygame.K_UP]:  # Up arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0], self.game.points[i][1] + 10)
            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x, obj.rect.y + 10, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0], obj.points[i][1] + 10)

            self.y += 10

        if keys[pygame.K_DOWN]:  # Down arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0], self.game.points[i][1] - 10)

            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x, obj.rect.y - 10, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0], obj.points[i][1] - 10)

            self.y -= 10

    def add_movement_particles(self):

        for _ in range(2):  # Adjust the number of particles as needed
            self.game.particle_system.add_particle(
                random.randint(0, self.game.width), random.randint(0, self.game.height),
                0, 0,
                100, random.randint(1, 2),  # lifespan and size
                random.randint(150, 255), random.randint(150, 255), random.randint(150, 255), 180,  # color and alpha
                'circle'  # shape
            )