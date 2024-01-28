import pygame

class Particle:
    def __init__(self, x, y, vx, vy, lifespan, size, red, green, blue):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifespan = lifespan
        self.size = size
        self.red = red
        self.green = green
        self.blue = blue

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 2

    def draw(self, screen):
        pygame.draw.circle(screen, (self.red, self.green, self.blue), (self.x, self.y), self.size)

class UnityParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, vx, vy, lifespan, size, red, green, blue):
        self.particles.append(Particle(x, y, vx, vy, lifespan, size, red, green, blue))

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)