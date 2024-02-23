import pygame
from gui import button
from gui import menu_buttons as dm
from classes import parkinson as particles
import random
from gui.button_animation import ButtonAnimation

class Settings_screen:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen

        self.particle_system = particles.UnityParticleSystem()

        self.mixer = self.game.mixer

        self.objects = []

        self.dimentions = [{'WIDTH': 2560, 'HEIGHT': 1440}, {'WIDTH': 1920, 'HEIGHT': 1080},
                           {'WIDTH': 1280, 'HEIGHT': 720}, {'WIDTH': 1000, 'HEIGHT': 700}]
        self.HotbarPositions = ['Bottom', 'Top', 'Left', 'Right']

        self.Fullscreen = [{'FULLSCREEN': 'ON'}, {'FULLSCREEN': 'OFF'}]

        self.Flashlight = [{'HD_Flashlight': 'ON'}, {'HD_Flashlight': 'OFF'}]

        from classes.font import Font
        self.font2 = pygame.font.Font(Font, self.width // 40)

        self.font = pygame.font.Font(Font, self.width // 20)

        self.maintext = self.font.render('Settings', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (self.width // 2, (self.height // 2) - (3 * self.height // 8))

        gapsize = self.height//50 + self.height//47


        self.resolutiontext = self.font2.render('Resolution:', True, 'white')
        self.resolutiontextRect = self.resolutiontext.get_rect()
        self.resolutiontextRect.center = (
        self.width // 2 - self.width // 7, self.height // 4 + gapsize)

        self.FStext = self.font2.render('Fullscreen:', True, 'white')
        self.FStextRect = self.FStext.get_rect()
        self.FStextRect.center = (
        self.width // 2 - self.width // 7, self.height // 4 + (self.width // 20 + self.height // 47) + gapsize)

        self.hottext = self.font2.render('Hotbar location:', True, 'white')
        self.hottextRect = self.hottext.get_rect()

        self.hottextRect.center = (self.width // 2 - self.width // 7,  self.height // 4 + 2 * (self.width // 20 + self.height // 47) + gapsize)

        self.flashlighttext = self.font2.render('HD Flashlight:', True, 'white')
        self.flashlighttextRect = self.flashlighttext.get_rect()

        self.flashlighttextRect.center = (self.width // 2 - self.width // 7,  self.height // 4 + 3 * (self.width // 20 + self.height // 47) + gapsize)

        self.musictext = self.font2.render('Music Settings:', True, 'white')
        self.musictextrect = self.musictext.get_rect()

        self.musictextrect.center = (self.width // 2 - self.width // 7,  self.height // 4 + 4 * (self.width // 20 + self.height // 47) + gapsize)

        save_n_exit = button.ButtonForgame(71, self)
        self.save_n_exit_animation = ButtonAnimation(save_n_exit, save_n_exit.rect.x*6+(save_n_exit.width//2), save_n_exit.rect.y)

        self.Menu_buttons = []

        self.Menu_buttons = [dm.ButtonMenus(self, x) for x in range(5)]

        self.game.objects.append(self)


    def render(self):
        self.screen.blit(self.resolutiontext, self.resolutiontextRect)
        self.screen.blit(self.hottext, self.hottextRect)
        self.screen.blit(self.maintext, self.maintextRect)
        self.screen.blit(self.FStext, self.FStextRect)
        self.screen.blit(self.flashlighttext, self.flashlighttextRect)
        self.screen.blit(self.musictext, self.musictextrect)

        self.generate_particles()
        self.particle_system.update()
        self.particle_system.draw(self.screen)

        self.save_n_exit_animation.animate()
        for object in self.objects:
            object.render()

    def checkevent(self, pos):
        for object in self.objects:
            object.checkcollision(pos)

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




