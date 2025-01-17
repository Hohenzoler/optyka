import os
import random
from classes import images
import pygame
from gui import button
import settingsSetup
from screens import settings_screen, loading_saves_screen, achievements_screen, music_settings
from classes import parkinson as particles
from gui.button_animation import ButtonAnimation
from classes import mixer_c

pygame.init()

class StartScreen:
    def __init__(self, version):
        self.save_to_load = None

        self.version = version

        settings = settingsSetup.load_settings()

        self.settings = settings

        self.mixer = mixer_c.Mixer(settings)
        self.mixer.soundtrack()

        self.particle_system = particles.UnityParticleSystem()
        self.width = settings['WIDTH']
        self.height = settings['HEIGHT']
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.mouse.set_visible(False)  # Hide the default mouse cursor
        self.cursor_img = images.bad_coursor  # Custom cursor image
        self.cursor_img_rect = self.cursor_img.get_rect()  # Rectangle for the custom cursor image

        self.screen_mode = None

        self.settings_fullscreen = settings['FULLSCREEN']

        if self.settings_fullscreen == 'ON':
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

        self.run = True
        self.mode = 'default'
        self.objects = []
        from classes.font import Font
        self.font = pygame.font.Font(Font, self.width//20)
        self.version_font = pygame.font.Font(Font, self.width // 50)

        from classes import fps
        self.fps = fps.return_fps()

        self.tick = int((1 / self.fps) * 1000)

        self.clock = pygame.time.Clock()

        self.executed_functions = 'default'

        self.maintext = self.font.render('Optics', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width // 2, (self.height // 2) - (3 * self.height // 10))

        self.versiontext = self.version_font.render(f"Optics {self.version}", True, 'white')
        self.versiontextRect = self.versiontext.get_rect()
        self.versiontextRect.center = ((self.versiontextRect[2]//2) + self.versiontextRect[3], self.height - self.versiontextRect[3])

        self.buttons = [button.ButtonForgame(x, self) for x in range(4)]
        self.button_animations = [ButtonAnimation(b, b.rect.x*6+(b.width//2), b.rect.y) for i, b in enumerate(self.buttons)]

        pygame.display.set_caption('Optics')

        self.selected_buttons = {}

        self.preset = False

        self.mainloop()


    def mainloop(self):
        while self.run:

            if self.mode == 'default':
                self.generate_particles()
                self.defualt_mode()
                for animation in self.button_animations:
                    animation.animate()

            elif self.mode == 'settings':
                self.settings_mode()

            elif self.mode == 'achievements':
                self.achievements_mode()

            elif self.mode == 'load_new_settings':
                self.load_new_settings()

            elif self.mode == 'loading':
                self.load_mode()
            
            elif self.mode == 'delete':
                self.delete()

            elif self.mode == 'music':
                self.music()


            self.checkforevents()
            self.render()

            self.clock.tick(self.fps)

        for key, value in self.selected_buttons.items():
            if value == True:
                self.save_to_load = key

    def checkforevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for object in self.objects:
                    if type(object) == button.ButtonForgame and event.button == 1:
                        object.checkcollision(event.pos)
                    elif type(object) == settings_screen.Settings_screen or type(object) == loading_saves_screen.Loading_saves_screen or type(object) == achievements_screen.AchievementsScreen or type(object) == music_settings.Music_settings_screen and event.button == 1:
                        object.checkevent(event.pos)
                    elif type(object) == loading_saves_screen.saveselector:
                        if event.button == 4 and object.scrolling_needed:
                            if object.scroll_offset > 0:
                                object.scroll_offset -= 1
                        elif event.button == 5 and object.scrolling_needed:
                            if self.screen_mode.state == 'default':
                                object.max_offset = max(0, len(object.saves_files) - object.num_of_buttons)
                            elif self.screen_mode.state == 'presets':
                                object.max_offset = max(0, len(object.presets) - object.num_of_buttons)
                            if object.scroll_offset < object.max_offset:
                                object.scroll_offset += 1
                    elif type(object) == loading_saves_screen.saveselector.Button_v2:
                        if event.button == 1:
                            if object.rect.collidepoint(event.pos):
                                for (key, value) in self.selected_buttons.items():
                                    if value == True and key != object.text:
                                        self.selected_buttons[key] = False
                                object.selected_buttons[object.text] = not object.selected_buttons[object.text]
                    elif type(object) == loading_saves_screen.saveselector.Slider:
                        if event.button == 4:
                            object.slider_pos = max(0, object.slider_pos - 1)
                        elif event.button == 5:
                            object.slider_pos = min(object.num_sections - 1, object.slider_pos + 1)
    def render(self):
        self.screen.fill('black')
        self.particle_system.update()
        self.particle_system.draw(self.screen)
        for object in self.objects:
            object.render()

        if self.mode == 'default':
            self.screen.blit(self.maintext, self.maintextRect)
            self.screen.blit(self.versiontext, self.versiontextRect)

        self.cursor_img_rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, self.cursor_img_rect)
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

            self.buttons = [button.ButtonForgame(x, self) for x in range(4)]
            self.button_animations = [ButtonAnimation(b, b.rect.x*6+(b.width//2), b.rect.y) for i, b in enumerate(self.buttons)]
            self.executed_functions = 'default'

    def achievements_mode(self):
        if self.executed_functions != 'achievements':
            self.buttons = []
            self.objects = []
            self.screen_mode = achievements_screen.AchievementsScreen(self)
            self.screen_mode.render()
            self.executed_functions = 'achievements'


    def settings_mode(self):
        if self.executed_functions != 'settings':
            self.buttons = []

            self.objects = []

            self.screen_mode = None
            self.screen_mode = settings_screen.Settings_screen(self)

            self.executed_functions = 'settings'

    def load_mode(self):
        if self.executed_functions != 'loading':
            self.buttons = []

            self.objects = []

            self.screen_mode = None
            self.screen_mode = loading_saves_screen.Loading_saves_screen(self)

            self.executed_functions = 'loading'

    def load_new_settings(self):

        settings = settingsSetup.load_settings()

        self.settings = settings

        self.width = settings['WIDTH']
        self.height = settings['HEIGHT']


        from classes.font import Font
        self.font = pygame.font.Font(Font, self.width // 20)

        self.maintext = self.font.render('Optics', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width//2, (self.height//2) - (3 * self.height//10))

        self.version_font = pygame.font.Font(Font, self.width // 50)

        self.versiontext = self.version_font.render(f"Optics {self.version}", True, 'white')
        self.versiontextRect = self.versiontext.get_rect()
        self.versiontextRect.center = (
        (self.versiontextRect[2] // 2) + self.versiontextRect[3], self.height - self.versiontextRect[3])

        if settings['FULLSCREEN'] == 'ON':
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=0)
        else:
                self.screen = pygame.display.set_mode((self.width, self.height), vsync=0)

        self.mode = 'default'

    def delete(self):
        if self.executed_functions != 'delete':
            for idx, (key, value) in enumerate(self.selected_buttons.items()):
                if value == True:
                    os.remove(f'saves/{key}.json')
            self.executed_functions = 'delete'
            self.mode = 'loading'

    def music(self):
        if self.executed_functions != 'music':
            self.buttons = []

            self.objects = []

            self.screen_mode = music_settings.Music_settings_screen(self)

            self.executed_functions = 'music'
