import pygame
import sys
import settingsSetup


class ButtonMenus:
    def __init__(self, StartScreen, number):
        self.ss = StartScreen
        self.screen = self.ss.screen
        self.options = []
        self.width = self.ss.width // 5
        self.height = self.ss.width // 20
        gap_size = self.ss.height//47
        self.x = self.ss.width // 2 + self.width // 3
        self.y = self.ss.height // 4 + number * (self.height + gap_size)
        from classes.font import Font
        self.font = pygame.font.Font(Font, self.height // 3)
        self.text_color = 'white'
        self.menu_color = 'darkgrey'
        self.number = number
        self.selected_option_2 = None
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.ss.objects.append(self)

        if self.number == 0:

            self.dimention_width = self.ss.width
            self.dimention_height = self.ss.height
            self.options.append(f'{self.dimention_width}x{self.dimention_height}')

            for dimention in self.ss.dimentions:
                self.dimention_width = dimention['WIDTH']
                self.dimention_height = dimention['HEIGHT']
                dimensions = f'{self.dimention_width}x{self.dimention_height}'
                if dimensions not in self.options:
                    self.options.append(dimensions)

            self.options = sorted(self.options, key=lambda x: int(x.split('x')[0]), reverse=False)
            self.selected_option_2 = f'{self.ss.width}x{self.ss.height}'



        elif self.number == 2:
            for positon in self.ss.HotbarPositions:
                self.options.append(positon)
            s = settingsSetup.load_settings()
            self.selected_option_2 = s['HOTBAR_POSITION'].capitalize()
        elif self.number == 1:
            for option in self.ss.Fullscreen:
                self.options.append(option['FULLSCREEN'])

            s = settingsSetup.load_settings()

            self.selected_option_2 = s['FULLSCREEN']
        elif self.number == 3:
            for option in self.ss.Flashlight:
                self.options.append(option['HD_Flashlight'])

            s = settingsSetup.load_settings()

            self.selected_option_2 = s['HD_Flashlight']

        elif self.number == 4:
            self.options.append('Change')
            self.selected_option_2 = 'Change'

        self.current_index = 0

        for idx, option in enumerate(self.options):
            if option == self.selected_option_2:
                self.current_index = idx

    def render(self):
        pygame.draw.rect(self.screen, (55, 55, 55), (self.x, self.y, self.width, self.height), 0, 4)
        pygame.draw.rect(self.screen, self.text_color, (self.x, self.y, self.width, self.height), 2, 4)
        option_text = self.font.render(self.selected_option_2, True, self.text_color)
        option_text_rect = option_text.get_rect(center=self.rect.center)
        self.screen.blit(option_text, option_text_rect)


    def checkcollision(self, pos):

        if self.rect.collidepoint(pos):
            self.handle_button_click(self.options[(self.current_index + 1) % len(self.options)])

    def handle_button_click(self, option):
        self.ss.mixer.clicked_sound()
        if self.number == 0:
            self.selected_option_2 = option
            width, height = option.split('x')

            s = settingsSetup.load_settings()

            s['WIDTH'] = int(width)
            s['HEIGHT'] = int(height)

            settingsSetup.writesettingstofile(s)


        elif self.number == 2:
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

        elif self.number == 3:
            self.selected_option_2 = option

            s = settingsSetup.load_settings()

            s['HD_Flashlight'] = option

            settingsSetup.writesettingstofile(s)
            settingsSetup.settings['HD_Flashlight'] = option

        elif self.number == 4:
            self.ss.game.mode = 'music'

        self.current_index += 1
