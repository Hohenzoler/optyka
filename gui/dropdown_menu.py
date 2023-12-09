import pygame
import sys
import json

class DropdownMenu:
    def __init__(self, StartScreen, number):
        self.ss = StartScreen
        self.screen = self.ss.screen
        self.options = []
        self.width = self.ss.width // 5
        self.height = self.ss.width // 20
        gap_size = 15
        self.x = self.ss.width // 2 + self.width // 2
        self.y = self.ss.height // 2 - number * (self.height + gap_size)  # Adjusted y based on the number and gap size
        self.font = pygame.font.Font(None, self.height // 2)
        self.text_color = 'white'
        self.menu_color = 'darkgrey'
        self.expanded = False
        self.selected_option = None
        self.number = number

        self.ss.objects.append(self)

        if self.number == 2:
            for dimention in self.ss.dimentions:
                self.options.append(f'{dimention['WIDTH']}x{dimention['HEIGHT']}')
        elif self.number == 1:
            for positon in self.ss.HotbarPositions:
                self.options.append(positon)

    def render(self):
        pygame.draw.rect(self.screen, self.menu_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.text_color, (self.x, self.y, self.width, self.height), 2)

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                pygame.draw.rect(self.screen, self.menu_color, option_rect)
                pygame.draw.rect(self.screen, self.text_color, option_rect, 2)

                option_text = self.font.render(option, True, self.text_color)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                self.screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        dropdown_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if dropdown_rect.collidepoint(event.pos):
            self.expanded = not self.expanded
        else:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                if option_rect.collidepoint(event.pos) and self.expanded:
                    self.selected_option = option
                    self.expanded = False
                    self.handle_button_click(option)

    def handle_button_click(self, option):
        if self.number == 2:
            width, height = option.split('x')

            with open('settings.json', 'r') as f:
                json_object = json.loads(f.read())
                f.close()
            s = json_object

            s['WIDTH'] = int(width)
            s['HEIGHT'] = int(height)

            print(width, height)

            json_string = json.dumps(s, indent=1)
            with open('settings.json', 'w') as f:
                f.write(json_string)
                f.close()


        elif self.number == 1:
            position = option

            with open('settings.json', 'r') as f:
                json_object = json.loads(f.read())
                f.close()
            s = json_object

            s['HOTBAR_POSITION'] = position

            json_string = json.dumps(s, indent=1)
            with open('settings.json', 'w') as f:
                f.write(json_string)
                f.close()

            print(position)



