import pygame
from gui import button
import settingsSetup
from classes import parkinson as particles
import random
from gui.button_animation import ButtonAnimation
from classes import mixer_c

class Music_settings_screen:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen
        self.mixer = self.game.mixer

        from classes.font import Font
        self.font = pygame.font.Font(Font, self.width // 20)
        self.font2 = pygame.font.Font(Font, self.width // 40)

        self.gapsize = self.height // 50 + self.height // 47

        self.objects = []

        self.state = 'default'
        self.action = None

        self.generate_text()

        self.volume_bars = [Volume_bar(self, x) for x in range(5)]

        self.back_button = button.ButtonForgame(71, self)
        self.back_button_animation = ButtonAnimation(self.back_button,
                                                     self.back_button.rect.x * 6 + (self.back_button.width // 2),
                                                     self.back_button.rect.y)

        self.particle_system = particles.UnityParticleSystem()

        self.game.objects.append(self)

    def render(self):
        self.generate_particles()
        self.particle_system.update()
        self.particle_system.draw(self.screen)

        self.back_button_animation.animate()


        self.screen.blit(self.maintext, self.maintextRect)
        self.screen.blit(self.mastervolume, self.mastervolume_rect)
        self.screen.blit(self.Soundtrack, self.SoundtrackRect)
        self.screen.blit(self.objectVolume, self.objectVolumeRect)
        self.screen.blit(self.actionVolume, self.actionVolumeRect)
        self.screen.blit(self.achievementVolume, self.achievementVolumeRect)



        if self.state == 'default':
            self.default()

        for object in self.objects:
            object.render()


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

    def default(self):
        if self.action != 'default':

            self.action = 'default'

    def checkevent(self, pos):
        for object in self.objects:
            object.checkcollision(pos)

    def generate_text(self):

        self.maintext = self.font.render('Music Settings', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width // 2, (self.height // 2) - (3 * self.height // 8))

        self.mastervolume = self.font2.render('Master Volume:', True, 'white')
        self.mastervolume_rect = self.mastervolume.get_rect()
        self.mastervolume_rect.center = (
        self.width // 2 - self.width // 4, self.height // 4 + self.gapsize)

        self.Soundtrack = self.font2.render('Soundtrack Volume:', True, 'white')
        self.SoundtrackRect = self.Soundtrack.get_rect()
        self.SoundtrackRect.center = (
            self.width // 2 - self.width // 4,
            self.height // 4 + (self.width // 20 + self.height // 47) + self.gapsize)

        self.objectVolume = self.font2.render('Object Volume:', True, 'white')
        self.objectVolumeRect = self.objectVolume.get_rect()
        self.objectVolumeRect.center = (
            self.width // 2 - self.width // 4,
            self.height // 4 + 2 * (self.width // 20 + self.height // 47) + self.gapsize)

        self.actionVolume = self.font2.render('Action Volume:', True, 'white')
        self.actionVolumeRect = self.actionVolume.get_rect()
        self.actionVolumeRect.center = (
            self.width // 2 - self.width // 4,
            self.height // 4 + 3 * (self.width // 20 + self.height // 47) + self.gapsize)

        self.achievementVolume = self.font2.render('Achievement Volume:', True, 'white')
        self.achievementVolumeRect = self.achievementVolume.get_rect()
        self.achievementVolumeRect.center = (
            self.width // 2 - self.width // 4,
            self.height // 4 + 4 * (self.width // 20 + self.height // 47) + self.gapsize)



class Volume_bar:
    def __init__(self, game, number):
        self.game = game

        self.number = number

        self.white = (255, 255, 255)
        self.grey = (150, 150, 150)
        self.green = (0, 255, 0)

        self.rect_width = self.game.width//33
        self.rect_height = self.game.height//14
        self.gap = self.game.width//200
        self.num_rects = 10

        self.button_width = self.game.width//20
        self.button_height = self.game.height//14

        self.y = self.game.height // 4 + self.number * (
                    self.game.width // 20 + self.game.height // 47) + self.game.gapsize - self.rect_height // 2
        self.button_y = self.game.height // 4 + self.number * (
                    self.game.width // 20 + self.game.height // 47) + self.game.gapsize - self.button_height // 2

        self.x = self.game.width // 2 + (self.num_rects * (self.gap + self.rect_width)) // 8
        self.plus_button_x = self.x + self.num_rects * (self.gap + self.rect_width)
        self.minus_button_x = self.x - self.gap - self.button_width

        self.get_volume_level()

        self.game.objects.append(self)

    def draw_volume_slider(self):
        for i in range(self.num_rects):
            rect_x = self.x + (self.rect_width + self.gap) * i
            if i < self.volume_level:
                pygame.draw.rect(self.game.screen, self.green, (rect_x, self.y, self.rect_width, self.rect_height))
            else:
                pygame.draw.rect(self.game.screen, self.grey, (rect_x, self.y, self.rect_width, self.rect_height))

    def draw_plus_button(self):
        pygame.draw.rect(self.game.screen, self.white, (self.plus_button_x, self.button_y, self.button_width, self.button_height))
        plus_text = self.game.font.render("+", True, (0, 0, 0))
        text_rect = plus_text.get_rect(
            center=(self.plus_button_x + self.button_width // 2, self.button_y + self.button_height // 2))
        self.game.screen.blit(plus_text, text_rect)

    def draw_minus_button(self):
        pygame.draw.rect(self.game.screen, self.white, (self.minus_button_x, self.button_y, self.button_width, self.button_height))
        minus_text = self.game.font.render("-", True, (0, 0, 0))
        text_rect = minus_text.get_rect(
            center=(self.minus_button_x + self.button_width // 2, self.button_y + self.button_height // 2))
        self.game.screen.blit(minus_text, text_rect)

    def checkcollision(self, pos):
        if self.plus_button_x <= pos[0] <= self.plus_button_x + self.button_width and self.button_y <= pos[1] <= self.button_y + self.button_height:
            if self.volume_level < self.num_rects:
                self.volume_level += 1
                self.change_volume()
        elif self.minus_button_x <= pos[0] <= self.minus_button_x + self.button_width and self.button_y <= pos[1] <= self.button_y + self.button_height:
            if self.volume_level > 0:
                self.volume_level -= 1
                self.change_volume()



    def render(self):
        self.draw_volume_slider()
        self.draw_plus_button()
        self.draw_minus_button()

    def change_volume(self):
        s = settingsSetup.load_settings()

        if self.number == 0:
            s['MASTER_VOLUME'] = self.volume_level / 10

        if self.number == 1:
            s['SOUNDTRACK_VOLUME'] = self.volume_level / 10

        if self.number == 2:
            s['OBJECT_VOLUME'] = self.volume_level / 10

        if self.number == 3:
            s['ACTION_VOLUME'] = self.volume_level / 10

        if self.number == 4:
            s['ACHIEVEMENT_VOLUME'] = self.volume_level / 10

        self.game.game.mixer = mixer_c.Mixer(s)
        self.game.game.mixer.soundtrack()
        settingsSetup.writesettingstofile(s)

    def get_volume_level(self):
        s = settingsSetup.load_settings()

        if self.number == 0:
            self.volume_level = s['MASTER_VOLUME'] * 10
        elif self.number == 1:
            self.volume_level = s['SOUNDTRACK_VOLUME'] * 10
        elif self.number == 2:
            self.volume_level = s['OBJECT_VOLUME'] * 10
        elif self.number == 3:
            self.volume_level = s['ACTION_VOLUME'] * 10
        elif self.number == 4:
            self.volume_level = s["ACHIEVEMENT_VOLUME"] * 10
        else:
            self.volume_level = 0


