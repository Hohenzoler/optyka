import pygame


class Particle:
    def __init__(self, x, y, vx, vy, lifespan, size, red, green, blue, alpha, shape):
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
        self.shape = shape

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 2
        if self.alpha > 0 and self.lifespan > 0:
            self.alpha -= self.alpha // (1/2*self.lifespan)

    def draw(self, screen):
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        if self.shape == 'circle':
            pygame.draw.circle(surface, (self.red, self.green, self.blue, self.alpha), (self.size, self.size),
                               self.size)
        if self.shape == 'square':
            pygame.draw.rect(surface, (self.red, self.green, self.blue, self.alpha),
                             pygame.Rect(0, 0, self.size * 2, self.size * 2))
        screen.blit(surface, (self.x - self.size, self.y - self.size))


class UnityParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, vx, vy, lifespan, size, red, green, blue, alpha, shape):
        self.particles.append(Particle(x, y, vx, vy, lifespan, size, red, green, blue, alpha, shape))

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
