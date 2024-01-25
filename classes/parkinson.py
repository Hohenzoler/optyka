import pygame

class Particle:
    def __init__(self, x, y, vx, vy, lifespan):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifespan = lifespan

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 150, 0), (self.x, self.y), 5)

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