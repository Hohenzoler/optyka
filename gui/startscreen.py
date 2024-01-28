import random

import pygame
from gui import button
import settingsSetup
from gui import settings_screen
from classes import parkinson as particles

pygame.init()

class StartScreen:
    def __init__(self, width, height):
        settings = settingsSetup.load_settings()
        self.particle_system = particles.UnityParticleSystem()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.settings_fullscreen = settings['FULLSCREEN']

        if self.settings_fullscreen == 'ON':
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

        self.run = True
        self.mode = 'default'
        self.objects = []
        from classes.font import Font
        self.font = pygame.font.Font(Font, self.width//20)

        from classes import fps
        self.fps = fps.return_fps()

        self.tick = int((1 / self.fps) * 1000)

        self.clock = pygame.time.Clock()

        self.executed_functions = 'default'

        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width // 2, (self.height // 2) - (3 * self.height // 10))

        self.buttons = [button.ButtonForgame(x, self) for x in range(3)]

        pygame.display.set_caption('Optyka')

        self.mainloop()


    def mainloop(self):
        while self.run:

            if self.mode == 'default':
                self.generate_particles()
                self.defualt_mode()

            elif self.mode == 'settings':
                self.settings_mode()

            elif self.mode == 'load_new_settings':
                self.load_new_settings()

            self.checkforevents()
            self.render()

            self.clock.tick(self.fps)

    def checkforevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for object in self.objects:
                    if type(object) == button.ButtonForgame:
                        object.checkcollision(event.pos)
                    elif type(object) == settings_screen.Settings_screen:
                        object.checkevent(event.pos)

    def render(self):
        self.screen.fill('black')
        self.particle_system.update()
        self.particle_system.draw(self.screen)
        for object in self.objects:
            object.render()

        if self.mode == 'default':
            self.screen.blit(self.maintext, self.maintextRect)


        pygame.display.update()

    def generate_particles(self):
        # Adjust the parameters as needed
        self.particle_system.add_particle(
            x=random.randint(0, self.width),
            y=random.randint(0, self.height),
            vx=random.uniform(-0.1, 0.1),
            vy=random.uniform(-0.1, 0.1),
            lifespan=1000,
            size=random.randint(1, 2),
            red=random.randint(150, 255),
            green=random.randint(150, 255),
            blue=random.randint(150, 255),
            alpha=100
        )

    def defualt_mode(self):
        if self.executed_functions != 'default':
            self.buttons = [button.ButtonForgame(x, self) for x in range(3)]
            self.executed_functions = 'default'

    def settings_mode(self):
        if self.executed_functions != 'settings':
            self.buttons = []

            self.objects = []

            self.settingsscreen = settings_screen.Settings_screen(self)

            self.executed_functions = 'settings'

    def load_new_settings(self):

        self.objects.remove(self.settingsscreen)

        settings = settingsSetup.load_settings()

        self.width = settings['WIDTH']
        self.height = settings['HEIGHT']

        from classes.font import Font
        self.font = pygame.font.Font(Font, self.width // 20)

        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width//2, (self.height//2) - (3 * self.height//10))

        if settings['FULLSCREEN'] == 'ON':
            # if settings['VSYNC'] == 'ON':
            #     self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=1)
            # else:
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=0)
        else:
            # if settings['VSYNC'] == 'ON':
            #     self.screen = pygame.display.set_mode((self.width, self.height), vsync=1)
            # else:
                self.screen = pygame.display.set_mode((self.width, self.height), vsync=0)

        self.mode = 'default'
