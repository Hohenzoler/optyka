import pygame
from gui import button


class loading_saves_screen:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen

        self.objects = []

        new_game_button = button.ButtonForgame(72, self)
        self.objects.append(new_game_button)

        load_game_button = button.ButtonForgame(73, self)
        self.objects.append(load_game_button)

        back_button = button.ButtonForgame(74, self)
        self.objects.append(back_button)

        self.game.objects.append(self)

    def render(self):
        for object in self.objects:
            object.render()
