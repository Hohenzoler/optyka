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

        self.font = self.game.font

        self.objects = []

        self.state = 'default'
        self.action = None

        self.back_button = button.ButtonForgame(71, self)
        self.back_button_animation = ButtonAnimation(self.back_button, self.back_button.rect.x * 6 + (self.back_button.width // 2),
                                                     self.back_button.rect.y)

        self.volume_bar = Volume_bar(self)

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


class Volume_bar:
    def __init__(self, game):
        self.game = game

        self.white = (255, 255, 255)
        self.grey = (150, 150, 150)
        self.green = (0, 255, 0)

        self.rect_width = 30
        self.rect_height = 50
        self.gap = 5
        self.num_rects = 10
        self.plus_button_width = 50
        self.plus_button_height = 50
        self.minus_button_width = 50
        self.minus_button_height = 50

        self.x = 100
        self.y = (self.game.height - self.rect_height) // 2
        self.plus_button_x = self.x + self.num_rects * (self.gap + self.rect_width)
        self.plus_button_y = (self.game.height - self.plus_button_height) // 2
        self.minus_button_x = self.x - self.gap - self.minus_button_width
        self.minus_button_y = (self.game.height - self.minus_button_height) // 2

        self.volume_level = 5

        self.game.objects.append(self)

    def draw_volume_slider(self):
        for i in range(self.num_rects):
            rect_x = self.x + (self.rect_width + self.gap) * i
            if i < self.volume_level:
                pygame.draw.rect(self.game.screen, self.green, (rect_x, self.y, self.rect_width, self.rect_height))
            else:
                pygame.draw.rect(self.game.screen, self.grey, (rect_x, self.y, self.rect_width, self.rect_height))

    def draw_plus_button(self):
        pygame.draw.rect(self.game.screen, self.white, (self.plus_button_x, self.plus_button_y, self.plus_button_width, self.plus_button_height))
        plus_text = self.game.font.render("+", True, (0, 0, 0))
        text_rect = plus_text.get_rect(
            center=(self.plus_button_x + self.plus_button_width // 2, self.plus_button_y + self.plus_button_height // 2))
        self.game.screen.blit(plus_text, text_rect)

    def draw_minus_button(self):
        pygame.draw.rect(self.game.screen, self.white, (self.minus_button_x, self.minus_button_y, self.minus_button_width, self.minus_button_height))
        minus_text = self.game.font.render("-", True, (0, 0, 0))
        text_rect = minus_text.get_rect(
            center=(self.minus_button_x + self.minus_button_width // 2, self.minus_button_y + self.minus_button_height // 2))
        self.game.screen.blit(minus_text, text_rect)

    def checkcollision(self, pos):
        if self.plus_button_x <= pos[0] <= self.plus_button_x + self.plus_button_width and self.plus_button_y <= pos[1] <= self.plus_button_y + self.plus_button_height:
            if self.volume_level < self.num_rects:
                self.volume_level += 1
                print(self.volume_level)
        elif self.minus_button_x <= pos[0] <= self.minus_button_x + self.minus_button_width and self.minus_button_y <= pos[1] <= self.minus_button_y + self.minus_button_height:
            if self.volume_level > 0:
                self.volume_level -= 1
                print(self.volume_level)


    def render(self):
        self.draw_volume_slider()
        self.draw_plus_button()
        self.draw_minus_button()
