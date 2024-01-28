import pygame
import sys
import json
from classes import sounds
import settingsSetup


class DropdownMenu:
    def __init__(self, StartScreen, number):
        self.ss = StartScreen
        self.screen = self.ss.screen
        self.options = []
        self.width = self.ss.width // 5
        self.height = self.ss.width // 20
        gap_size = self.ss.height//47
        self.x = self.ss.width // 2 + self.width // 2
        self.y = self.ss.height // 2 - number * (self.height + gap_size)  # Adjusted y based on the number and gap size
        from classes.font import Font
        self.font = pygame.font.Font(Font, self.height // 2)
        self.text_color = 'white'
        self.menu_color = 'darkgrey'
        self.expanded = False
        self.selected_option = None
        self.number = number
        self.selected_option_2 = None
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.ss.objects.append(self)

        if self.number == 2:
            for dimention in self.ss.dimentions:
                self.dimention_width = dimention['WIDTH']
                self.dimention_height = dimention['HEIGHT']
                self.options.append(f'{self.dimention_width}x{self.dimention_height}')
            self.selected_option_2 = f'{self.ss.width}x{self.ss.height}'
        elif self.number == 0:
            for positon in self.ss.HotbarPositions:
                self.options.append(positon)
            s = settingsSetup.load_settings()
            self.selected_option_2 = s['HOTBAR_POSITION'].capitalize()
        elif self.number == 1:
            for option in self.ss.Fullscreen:
                self.options.append(option['FULLSCREEN'])

            s = settingsSetup.load_settings()

            self.selected_option_2 = s['FULLSCREEN']


    def render(self):
        pygame.draw.rect(self.screen, (55, 55, 55), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.text_color, (self.x, self.y, self.width, self.height), 2)
        option_text = self.font.render(self.selected_option_2, True, self.text_color)
        option_text_rect = option_text.get_rect(center=self.rect.center)
        self.screen.blit(option_text, option_text_rect)

        if self.expanded:
            # print(self.options)
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                pygame.draw.rect(self.screen, self.menu_color, option_rect)
                pygame.draw.rect(self.screen, self.text_color, option_rect, 2)

                option_text = self.font.render(option, True, self.text_color)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                self.screen.blit(option_text, option_text_rect)


    def checkcollision(self, pos):
        if self.rect.collidepoint(pos):
            self.expanded = not self.expanded
            sounds.clicked_sound()
        else:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                if option_rect.collidepoint(pos) and self.expanded:
                    self.selected_option = option
                    self.expanded = False
                    self.handle_button_click(option)

    def handle_button_click(self, option):
        sounds.clicked_sound()
        if self.number == 2:
            self.selected_option_2 = option
            width, height = option.split('x')

            s = settingsSetup.load_settings()

            s['WIDTH'] = int(width)
            s['HEIGHT'] = int(height)

            # print(width, height)

            settingsSetup.writesettingstofile(s)


        elif self.number == 0:
            position = option.lower()
            self.selected_option_2 = option

            s = settingsSetup.load_settings()

            s['HOTBAR_POSITION'] = position

            settingsSetup.writesettingstofile(s)

        elif self.number == 1:
            self.selected_option_2 = option

            s = settingsSetup.load_settings()

            s['FULLSCREEN'] = option

            settingsSetup.writesettingstofile(s)
