import random

import pygame

class Particle:
    def __init__(self, x, y, vx, vy, lifespan):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifespan = lifespan
        self.size = random.randint(1, 7)
        self.red = random.randint(130, 255)
        self.green = random.randint(0, 130)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 2

    def draw(self, screen):
        pygame.draw.circle(screen, (self.red, self.green, 0), (self.x, self.y), self.size)

class UnityParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, vx, vy, lifespan):
        self.particles.append(Particle(x, y, vx, vy, lifespan))

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)