import pygame
from gui import button
import os


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

        saveselector(self.game)

        self.game.objects.append(self)

    def render(self):
        for object in self.objects:
            object.render()

    def checkevent(self, pos):
        for object in self.objects:
            object.checkcollision(pos)

class saveselector:
    def __init__(self, game):
        self.game = game
        self.screen_width = self.game.width
        self.screen_height = self.game.height
        self.button_width = int(self.screen_width*0.63)
        self.button_height = int(self.screen_height*0.13)
        self.container_width = int(self.screen_width*0.75)
        self.container_height = int(self.screen_height*(2/3))
        self.scrollspeed = 30
        self.num_of_buttons = 3
        self.spacing = 20

        self.screen = self.game.screen

        self.dir = "saves"
        self.saves_files = [file for file in os.listdir(self.dir) if file.endswith('.json')]
        self.scrolling_needed = len(self.saves_files) > self.num_of_buttons
        self.scroll_offset = 0

        self.buttons = []
        for i in range(self.num_of_buttons):
            if i < len(self.saves_files):
                button1 = (self.Button_v2(self.game, self.saves_files[i], (self.screen_width - self.button_width) // 2, (self.screen_height - self.container_height - 150) // 2 + i * (self.button_height + self.spacing) + self.spacing, self.button_width, self.button_height))
                self.buttons.append(button1)

        self.container_rect = pygame.Rect((self.screen_width - self.container_width) // 2, (self.screen_height - self.container_height) // 2, self.container_width, self.container_height)

        self.game.objects.append(self)

    def render(self):
        for i, button in enumerate(self.buttons):
            button.rect.y = (self.screen_height - self.container_height) // 2 + i * (self.button_height + self.spacing) + self.spacing
            if button.is_visible(self.container_rect):
                if i + self.scroll_offset < len(self.saves_files):
                    button.text = self.saves_files[i + self.scroll_offset]
                button.render()

    class Button_v2:
        def __init__(self, game, text, x, y, width, height):
            self.game = game
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = (200, 200, 200)
            self.outline_color = (0, 0, 0)
            self.outline_thickness = 2

            self.game.objects.append(self)

        def render(self):
            pygame.draw.rect(self.game.screen, self.color, self.rect)
            pygame.draw.rect(self.game.screen, self.outline_color, self.rect, self.outline_thickness)
            text_surface = self.game.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.game.screen.blit(text_surface, text_rect)

        def is_visible(self, container_rect):
            return container_rect.contains(self.rect)

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)

