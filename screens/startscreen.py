import random

import pygame
from gui import button
import settingsSetup
from screens import settings_screen, loading_saves_screen
from classes import parkinson as particles

pygame.init()

class StartScreen:
    def __init__(self):
        self.save_to_load = None
        settings = settingsSetup.load_settings()
        self.particle_system = particles.UnityParticleSystem()
        self.width = settings['WIDTH']
        self.height = settings['HEIGHT']
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.screen_mode = None

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
        self.action = None

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

            elif self.mode == 'loading':
                self.load_mode()

            self.checkforevents()
            self.render()

            self.clock.tick(self.fps)

    def checkforevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for object in self.objects:
                    if type(object) == button.ButtonForgame:
                        object.checkcollision(event.pos)
                    elif type(object) == settings_screen.Settings_screen or type(object) == loading_saves_screen.loading_saves_screen:
                        object.checkevent(event.pos)
                    elif type(object) == loading_saves_screen.saveselector:
                        if event.button == 4 and object.scrolling_needed:
                            if object.scroll_offset > 0:
                                object.scroll_offset -= 1
                        elif event.button == 5 and object.scrolling_needed:
                            object.max_offset = max(0, len(object.saves_files) - object.num_of_buttons)
                            if object.scroll_offset < object.max_offset:
                                object.scroll_offset += 1
                        elif event.button == 1:
                            for button1 in object.buttons:
                                if button1.rect.collidepoint(event.pos):
                                    self.run = False
                                    self.save_to_load = button1.text

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
            alpha=100,
            shape='circle'
        )

    def defualt_mode(self):
        if self.executed_functions != 'default':
            if self.screen_mode != None:
                self.objects = []
                self.screen_mode = None

            self.buttons = [button.ButtonForgame(x, self) for x in range(3)]
            self.executed_functions = 'default'


    def settings_mode(self):
        if self.executed_functions != 'settings':
            self.buttons = []

            self.objects = []

            self.screen_mode = settings_screen.Settings_screen(self)

            self.executed_functions = 'settings'

    def load_mode(self):
        if self.executed_functions != 'loading':
            self.buttons = []

            self.objects = []

            self.screen_mode = loading_saves_screen.loading_saves_screen(self)

            self.executed_functions = 'loading'

    def load_new_settings(self):

        settings = settingsSetup.load_settings()

        self.width = settings['WIDTH']
        self.height = settings['HEIGHT']

        from classes.font import Font
        self.font = pygame.font.Font(Font, self.width // 20)

        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width//2, (self.height//2) - (3 * self.height//10))

        if settings['FULLSCREEN'] == 'ON':
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=0)
        else:
                self.screen = pygame.display.set_mode((self.width, self.height), vsync=0)

        self.mode = 'default'
