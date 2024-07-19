import pygame
from gui import button
import os, json
from classes import parkinson as particles
import random
from gui.button_animation import ButtonAnimation
from datetime import datetime
from classes.font import Font

class Loading_saves_screen:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen
        self.mixer = self.game.mixer

        self.state = 'default'
        self.action = None

        self.particle_system = particles.UnityParticleSystem()

        self.savesS = saveselector(self.game)

        self.game.objects.append(self)

    def render(self):
        self.generate_particles()
        self.particle_system.update()
        self.particle_system.draw(self.screen)

        if self.state == 'default':
            self.default()

        elif self.state == 'presets':
            self.presets()


        for animation in self.button_animations:
            animation.animate()
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

    def default(self):
        if self.action != 'default':
            self.objects = []
            new_game_button = button.ButtonForgame(72, self)

            load_preset_button = button.ButtonForgame(73, self)

            back_button = button.ButtonForgame(74, self)

            del_button = button.ButtonForgame(75, self)

            self.buttons = [new_game_button, load_preset_button, back_button, del_button]

            self.button_animations = [ButtonAnimation(b, b.rect.x, (b.rect.y - b.height)) for i, b in
                                      enumerate(self.buttons)]

            self.action = 'default'

    def presets(self):
        if self.action != 'presets':
            self.objects = []
            new_game_button = button.ButtonForgame(72, self)
            self.objects.append(new_game_button)

            back_button = button.ButtonForgame(74, self)
            self.objects.append(back_button)

            self.buttons = [new_game_button, back_button, ]

            self.button_animations = [ButtonAnimation(b, b.rect.x, (b.rect.y - b.height)) for i, b in
                                      enumerate(self.buttons)]
            self.action = 'presets'

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
        self.preset_dir = 'presets'

        self.container_rect = pygame.Rect((self.screen_width - self.container_width) // 2, (self.screen_height - self.container_height) // 2, self.container_width, self.container_height)

        self.game.objects.append(self)

    def get_Dates(self):
        a = []
        if self.game.screen_mode.state == 'default':
            for file in self.saves_files:
                file_path = f'{self.dir}/{file}.json'
                first_element = self.extract_first_element_from_json_file(file_path)
                a.append(first_element)
            a = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in a]
        elif self.game.screen_mode.state == 'presets':
            for file in self.presets:
                file_path = f'{self.preset_dir}/{file}.json'
                first_element = self.extract_first_element_from_json_file(file_path)
                a.append(first_element)
        return a

    def extract_first_element_from_json_file(self, file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    if type(data[0]) == str:
                        f.close()
                        return data[0]
                else:
                    return None

            except:
                f.close()
                return '1970-1-1 0:0:0'

    def render(self):

        if self.game.screen_mode.state == 'default' and self.game.screen_mode.action != 'default':
            self.remove_buttons_from_objects()
            self.generate_saves_buttons()

        elif self.game.screen_mode.state == 'default' and self.game.screen_mode.action == 'default':
            for i, button in enumerate(self.buttons):
                self.target_positions[i] = (self.screen_height - self.container_height) // 2 + i * (
                            self.button_height + self.spacing) + self.spacing
                ButtonAnimation(button, button.rect[0], self.target_positions[i]).animate()
                if button.is_visible(self.container_rect):
                    if i + self.scroll_offset < len(self.saves_files):
                        button.text = self.saves_files[i + self.scroll_offset]
                        button.date = self.dates[i + self.scroll_offset]
                    button.render()

        elif self.game.screen_mode.action != 'presets' and self.game.screen_mode.state == 'presets':
            self.remove_buttons_from_objects()
            self.generate_presets_buttons()

        elif self.game.screen_mode.state == 'presets' and self.game.screen_mode.action == 'presets':
            for i, button in enumerate(self.presets_buttons):
                self.target_positions[i] = (self.screen_height - self.container_height) // 2 + i * (
                            self.button_height + self.spacing) + self.spacing
                ButtonAnimation(button, button.rect[0], self.target_positions[i]).animate()
                if button.is_visible(self.container_rect):
                    if i + self.scroll_offset < len(self.presets):
                        # print(self.scroll_offset + i, len(self.presets))
                        button.text = self.presets[i + self.scroll_offset]
                        button.date = self.presets_date_title_thingy[i + self.scroll_offset]
                    button.render()


    def generate_saves_buttons(self):

        self.saves_files = [file[:-5] for file in os.listdir(self.dir) if file.endswith('.json')]

        self.dates = self.get_Dates()

        zipped = list(zip(self.dates, self.saves_files))

        sorted_zipped = sorted(zipped, key=lambda x: x[0], reverse=True)

        try:
            self.dates, self.saves_files = zip(*sorted_zipped)
        except:
            self.dates = []
            self.saves_files = []
            print("no saves ;(")

        self.dates = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in self.dates]

        self.scrolling_needed = len(self.saves_files) > self.num_of_buttons
        self.scroll_offset = 0

        for file in self.saves_files:
            self.game.selected_buttons[file] = False

        self.buttons = []
        for i in range(self.num_of_buttons):
            if i < len(self.saves_files):
                button1 = (self.Button_v2(self.game, self.saves_files[i], self.dates[i],
                                          (self.screen_width - self.button_width) // 2,
                                          (self.screen_height - self.container_height - 150) // 2 + i * (
                                                      self.button_height + self.spacing) + self.spacing,
                                          self.button_width, self.button_height, self.game.selected_buttons))
                self.buttons.append(button1)

        self.target_positions = [button.rect.y for button in self.buttons]

        if len(self.saves_files) > self.num_of_buttons:
            s = self.Slider(self)

    def generate_presets_buttons(self):

        self.presets = [file[:-5] for file in os.listdir(self.preset_dir) if file.endswith('.json')]
        self.presets.sort()
        self.presets_date_title_thingy = self.get_Dates()

        self.scrolling_needed = len(self.presets) > self.num_of_buttons
        print(self.scrolling_needed)
        self.scroll_offset = 0

        for file in self.presets:
            self.game.selected_buttons[file] = False

        self.presets_buttons = []
        for i in range(self.num_of_buttons):
            if i < len(self.presets):
                button1 = (self.Button_v2(self.game, self.presets[i], self.presets_date_title_thingy[i],
                                          (self.screen_width - self.button_width) // 2,
                                          (self.screen_height - self.container_height - 150) // 2 + i * (
                                                  self.button_height + self.spacing) + self.spacing,
                                          self.button_width, self.button_height, self.game.selected_buttons))
                self.presets_buttons.append(button1)

        self.target_positions = [button.rect.y for button in self.presets_buttons]

        if len(self.presets) > self.num_of_buttons:
            s = self.Slider(self)
    def remove_buttons_from_objects(self):
        i = []
        for idx, object in enumerate(self.game.objects):
            if type(object) == self.Button_v2 or type(object) == self.Slider:
                i.append(idx)
        i.reverse()
        for index in i:
            self.game.objects.remove(self.game.objects[index])
        self.game.selected_buttons = {}
    class Button_v2:
        def __init__(self, game, text, date, x, y, width, height, selected_buttons):
            self.game = game
            self.text = text
            self.date = date
            self.rect = pygame.Rect(x, y, width, height)
            self.color = (200, 200, 200)
            self.outline_color = (0, 255, 0)
            self.outline_thickness = 5

            self.selected_buttons = selected_buttons

            self.font = pygame.font.Font(Font, self.game.height//20)
            self.date_font = pygame.font.Font(Font, self.game.height//40)

            self.game.objects.append(self)

        def render(self):
            pygame.draw.rect(self.game.screen, self.color, self.rect, 0, 7)
            if self.selected_buttons[self.text] == True:
                pygame.draw.rect(self.game.screen, self.outline_color, self.rect, self.outline_thickness, 7)

            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 15))

            date_surface = self.date_font.render(self.date, True, (0, 0, 0))
            date_rect = date_surface.get_rect(center=(self.rect.centerx, self.rect.centery + text_rect.height * 0.5))

            self.game.screen.blit(text_surface, text_rect)
            self.game.screen.blit(date_surface, date_rect)

        def is_visible(self, container_rect):
            return container_rect.contains(self.rect)

    class Slider:
        def __init__(self, loading_save_screen):
            self.display = loading_save_screen

            if self.display.game.screen_mode.state == 'default':
                self.num_sections = len(self.display.saves_files) - 2
            elif self.display.game.screen_mode.state == 'presets':
                self.num_sections = len(self.display.presets) - 2

            self.section_height = (self.display.button_height * 0.9 * 3 + self.display.spacing * 3) // self.num_sections
            self.slider_height = self.section_height
            self.slider_pos = 0
            self.screen = self.display.game.screen
            self.display.game.objects.append(self)
        def render(self):
            pygame.draw.rect(self.screen, (26, 26, 26), (((self.display.screen_width - self.display.button_width) // 2) + self.display.button_width + 20, self.display.target_positions[0] - 5, 20, self.section_height * self.num_sections), 3, 5)
            pygame.draw.rect(self.screen, (200, 200, 200), (((self.display.screen_width - self.display.button_width) // 2) + self.display.button_width + 20, self.slider_height*self.slider_pos + self.display.target_positions[0] - 5, 20, self.slider_height), 0,5)
