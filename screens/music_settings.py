import pygame
from gui import button
import os, json
from classes import parkinson as particles
import random
from gui.button_animation import ButtonAnimation

class Music_settings_screen:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen
        self.mixer = self.game.mixer

        self.objects = []

        self.state = 'default'
        self.action = None

        self.back_button = button.ButtonForgame(71, self)
        self.back_button_animation = ButtonAnimation(self.back_button, self.back_button.rect.x * 6 + (self.back_button.width // 2),
                                                     self.back_button.rect.y)

        self.particle_system = particles.UnityParticleSystem()

        self.game.objects.append(self)

    def render(self):
        self.generate_particles()
        self.particle_system.update()
        self.particle_system.draw(self.screen)

        self.back_button_animation.animate()

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
