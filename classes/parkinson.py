import pygame


class Particle:
    """
    A class used to represent a Particle

    ...

    Attributes
    ----------
    x : int
        x-coordinate of the particle
    y : int
        y-coordinate of the particle
    vx : int
        velocity in x-direction
    vy : int
        velocity in y-direction
    lifespan : int
        lifespan of the particle
    size : int
        size of the particle
    red : int
        red color value (0-255)
    green : int
        green color value (0-255)
    blue : int
        blue color value (0-255)
    alpha : int
        alpha (transparency) value (0-255)
    shape : str
        shape of the particle ('circle' or 'square')

    Methods
    -------
    update():
        Updates the particle's position and decreases its lifespan and alpha value
    draw(screen):
        Draws the particle on the given screen
    """
    def __init__(self, x, y, vx, vy, lifespan, size, red, green, blue, alpha, shape):
        """
        Constructs all the necessary attributes for the particle object.

        Parameters
        ----------
            x : int
                x-coordinate of the particle
            y : int
                y-coordinate of the particle
            vx : int
                velocity in x-direction
            vy : int
                velocity in y-direction
            lifespan : int
                lifespan of the particle
            size : int
                size of the particle
            red : int
                red color value (0-255)
            green : int
                green color value (0-255)
            blue : int
                blue color value (0-255)
            alpha : int
                alpha (transparency) value (0-255)
            shape : str
                shape of the particle ('circle' or 'square')
        """
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

    def update(self, x, y):
        """
        Updates the particle's position and decreases its lifespan and alpha value
        """
        self.x += self.vx
        self.x += x
        self.y += self.vy
        self.y += y
        if self.alpha > 0 and self.lifespan > 0:
            self.alpha -= self.alpha // (1/2*self.lifespan)
            self.lifespan -= 2

    def draw(self, screen):
        """
        Draws the particle on the given screen

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the particle is to be drawn
        """
        screen_width, screen_height = screen.get_size()  # Get the size of the screen
        if 0 <= self.x <= screen_width and 0 <= self.y <= screen_height:  # Check if the particle is within the screen
            surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            if self.shape == 'circle':
                pygame.draw.circle(surface, (self.red, self.green, self.blue, self.alpha), (self.size, self.size),
                                   self.size)
            elif self.shape == 'square':
                pygame.draw.rect(surface, (self.red, self.green, self.blue, self.alpha),
                                 pygame.Rect(0, 0, self.size * 2, self.size * 2))
            elif self.shape == 'triangle':
                pygame.draw.polygon(surface, (self.red, self.green, self.blue, self.alpha),
                                    [(self.size, 0), (0, self.size * 2), (self.size * 2, self.size * 2)])
            screen.blit(surface, (self.x - self.size, self.y - self.size))

class UnityParticleSystem:
    """
    A class used to represent a Unity Particle System

    ...

    Attributes
    ----------
    particles : list
        list of particles in the system

    Methods
    -------
    add_particle(x, y, vx, vy, lifespan, size, red, green, blue, alpha, shape):
        Adds a new particle to the system
    update():
        Updates all particles in the system
    draw(screen):
        Draws all particles in the system on the given screen
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the UnityParticleSystem object.
        """
        self.particles = []

    def add_particle(self, x, y, vx, vy, lifespan, size, red, green, blue, alpha, shape):
        """
        Adds a new particle to the system

        Parameters
        ----------
            x : int
                x-coordinate of the particle
            y : int
                y-coordinate of the particle
            vx : int
                velocity in x-direction
            vy : int
                velocity in y-direction
            lifespan : int
                lifespan of the particle
            size : int
                size of the particle
            red : int
                red color value (0-255)
            green : int
                green color value (0-255)
            blue : int
                blue color value (0-255)
            alpha : int
                alpha (transparency) value (0-255)
            shape : str
                shape of the particle ('circle' or 'square')
        """
        self.particles.append(Particle(x, y, vx, vy, lifespan, size, red, green, blue, alpha, shape))

    def update(self):
        """
        Updates all particles in the system
        """
        keys = pygame.key.get_pressed()  # Get the state of each key
        particle_x, particle_y = 0, 0
        if keys[pygame.K_RIGHT]:  # Right arrow key is held down
            particle_x = - 10
        if keys[pygame.K_LEFT]:  # Left arrow key is held down
            particle_x = 10
        if keys[pygame.K_UP]:  # Up arrow key is held down
            particle_y = 10
        if keys[pygame.K_DOWN]:  # Down arrow key is held down
            particle_y = -10
        for particle in self.particles:
            particle.update(particle_x, particle_y)
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        """
        Draws all particles in the system on the given screen

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the particles are to be drawn
        """
        for particle in self.particles:
            particle.draw(screen)
