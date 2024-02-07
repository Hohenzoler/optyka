import pygame
from gui import button
import os, json
from classes import parkinson as particles
import random
from gui.button_animation import ButtonAnimation
from datetime import datetime
from classes.font import Font

class loading_saves_screen:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen
        self.objects = []

        self.particle_system = particles.UnityParticleSystem()

        new_game_button = button.ButtonForgame(72, self)
        self.objects.append(new_game_button)

        load_game_button = button.ButtonForgame(73, self)
        self.objects.append(load_game_button)

        back_button = button.ButtonForgame(74, self)
        self.objects.append(back_button)

        saveselector(self.game)

        self.game.objects.append(self)

    def render(self):
        self.generate_particles()
        self.particle_system.update()
        self.particle_system.draw(self.screen)
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
        self.saves_files = [file[:-5] for file in os.listdir(self.dir) if file.endswith('.json')]

        self.dates = self.get_Dates()

        zipped = list(zip(self.dates, self.saves_files))

        sorted_zipped = sorted(zipped, key=lambda x: x[0], reverse=True)

        self.dates, self.saves_files = zip(*sorted_zipped)

        print("Sorted array1:", self.dates)
        print("Sorted array2:", self.saves_files)

        self.dates = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in self.dates]

        self.scrolling_needed = len(self.saves_files) > self.num_of_buttons
        self.scroll_offset = 0

        self.buttons = []
        for i in range(self.num_of_buttons):
            if i < len(self.saves_files):
                button1 = (self.Button_v2(self.game, self.saves_files[i], self.dates[i], (self.screen_width - self.button_width) // 2, (self.screen_height - self.container_height - 150) // 2 + i * (self.button_height + self.spacing) + self.spacing, self.button_width, self.button_height))
                self.buttons.append(button1)

        self.target_positions = [button.rect.y for button in self.buttons]

        self.container_rect = pygame.Rect((self.screen_width - self.container_width) // 2, (self.screen_height - self.container_height) // 2, self.container_width, self.container_height)

        if len(self.saves_files) > 3:
            s = self.Slider(self)

        self.game.objects.append(self)

    def get_Dates(self):
        a = []
        for file in self.saves_files:
            file_path = f'{self.dir}/{file}.json'
            first_element = self.extract_first_element_from_json_file(file_path)
            a.append(first_element)
        a = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in a]
        return a

    def extract_first_element_from_json_file(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            else:
                return None

    def render(self):
        for i, button in enumerate(self.buttons):
            self.target_positions[i] = (self.screen_height - self.container_height) // 2 + i * (
                        self.button_height + self.spacing) + self.spacing
            ButtonAnimation(button, button.rect.x, self.target_positions[i]).animate()
            if button.is_visible(self.container_rect):
                if i + self.scroll_offset < len(self.saves_files):
                    button.text = self.saves_files[i + self.scroll_offset]
                    button.date = self.dates[i + self.scroll_offset]
                button.render()

    class Button_v2:
        def __init__(self, game, text, date, x, y, width, height):
            self.game = game
            self.text = text
            self.date = date
            self.rect = pygame.Rect(x, y, width, height)
            self.color = (200, 200, 200)
            self.outline_color = (0, 0, 0)
            self.outline_thickness = 2

            self.font = pygame.font.Font(Font, self.game.height//20)
            self.date_font = pygame.font.Font(Font, self.game.height//40)

            self.game.objects.append(self)

        def render(self):
            pygame.draw.rect(self.game.screen, self.color, self.rect)
            pygame.draw.rect(self.game.screen, self.outline_color, self.rect, self.outline_thickness)

            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 20))

            date_surface = self.date_font.render(self.date, True, (0, 0, 0))
            date_rect = date_surface.get_rect(center=(self.rect.centerx, self.rect.centery + text_rect.height * 0.5))

            self.game.screen.blit(text_surface, text_rect)
            self.game.screen.blit(date_surface, date_rect)

        def is_visible(self, container_rect):
            return container_rect.contains(self.rect)

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)

    class Slider:
        def __init__(self, loading_save_screen):
            self.display = loading_save_screen
            self.num_sections = len(self.display.saves_files) - 2
            self.section_height = (self.display.button_height * 3 + self.display.spacing * 3) // self.num_sections
            self.slider_height = self.section_height
            self.slider_pos = 0
            self.screen = self.display.game.screen
            self.display.game.objects.append(self)
        def render(self):
            pygame.draw.rect(self.screen, (26, 26, 26), (((self.display.screen_width - self.display.button_width) // 2) + self.display.button_width + 20, self.display.target_positions[0] - 5, 20, self.section_height * self.num_sections))
            pygame.draw.rect(self.screen, (200, 200, 200), (((self.display.screen_width - self.display.button_width) // 2) + self.display.button_width + 20, self.slider_height*self.slider_pos + self.display.target_positions[0] - 5, 20, self.slider_height))
