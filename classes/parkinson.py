import pygame

class Particle:
    def __init__(self, x, y, vx, vy, lifespan, size, red, green, blue, alpha):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifespan = lifespan
        self.size = size
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.alpha > 0:
            self.alpha -= 1
        self.lifespan -= 2

    def draw(self, screen):
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)  # Create a surface
        pygame.draw.circle(surface, (self.red, self.green, self.blue, self.alpha), (self.size, self.size),
                           self.size)  # Draw the particle on the surface
        screen.blit(surface, (self.x - self.size, self.y - self.size))
class UnityParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, vx, vy, lifespan, size, red, green, blue, alpha):
        self.particles.append(Particle(x, y, vx, vy, lifespan, size, red, green, blue, alpha))

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)