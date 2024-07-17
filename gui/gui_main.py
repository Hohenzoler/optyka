import pygame
from gui import button
from classes import bin


class GUI:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height // 10
        self.position = self.game.settings['HOTBAR_POSITION']

        if self.position == 'bottom':
            self.rect = pygame.Rect(0, self.height * 10 - self.height, self.width, self.height)
        elif self.position == 'left':
            self.rect = pygame.Rect(0, 0, self.width // 10, self.height * 10)
            # self.game.achievements.handle_achievement_unlocked("U are weird...")
        elif self.position == 'right':
            self.rect = pygame.Rect(self.width - self.width // 10, 0, self.width // 10, self.height * 10)
            # self.game.achievements.handle_achievement_unlocked("U are weird...")
        elif self.position == 'top':
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            # self.game.achievements.handle_achievement_unlocked("U are weird...")

        self.layer = 3  # Assign a higher layer value to GUI to ensure it's rendered on top
        self.game.objects.append(self)
        self.f = None

        self.bin = bin.Bin(self.game)

        self.button_min = -3
        self.button_max = 7

        self.buttons = [button.Button(self.game, x, tooltip_text=self.tooltip_list(x)) for x in
                        range(self.button_min, self.button_max)]  # creates buttons
        self.transparent_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        self.draw_gradient(self.transparent_surface, (100, 100, 100, 200), (50, 50, 50, 200), "vertical")

    def draw_gradient(self, surface, start_color, end_color, gradient_direction="vertical"):
        """
        Draws a vertical or horizontal gradient on a surface, supporting transparency.

        :param surface: pygame.Surface to draw on.
        :param start_color: Tuple of RGBA values for the start color.
        :param end_color: Tuple of RGBA values for the end color.
        :param gradient_direction: String, either "vertical" or "horizontal" for the gradient direction.
        """
        start_r, start_g, start_b, start_a = start_color
        end_r, end_g, end_b, end_a = end_color
        width, height = surface.get_size()

        for i in range(height if gradient_direction == "vertical" else width):
            r = start_r + (end_r - start_r) * i / (height if gradient_direction == "vertical" else width)
            g = start_g + (end_g - start_g) * i / (height if gradient_direction == "vertical" else width)
            b = start_b + (end_b - start_b) * i / (height if gradient_direction == "vertical" else width)
            a = start_a + (end_a - start_a) * i / (height if gradient_direction == "vertical" else width)
            color = (int(r), int(g), int(b), int(a))
            pygame.draw.line(surface, color, (0, i) if gradient_direction == "vertical" else (i, 0),
                             (width, i) if gradient_direction == "vertical" else (i, height))
    # In the GUI class, modify the render method to use the gradient
    def render(self):

        # Apply a gradient instead of a solid fill
        self.game.screen.blit(self.transparent_surface, self.rect.topleft)
        for button in self.buttons:  # renders buttons
            button.render()

    def checkifclicked(self, mousepos):
        if self.game.selected_object is not None:
            return
        for button in self.buttons:
            button.checkifclicked(mousepos)

    def tooltip_list(self, id):
        if id == -3:
            return "Achievements"
        elif id == -2:
            return "Settings"
        elif id == -1:
            return "Quit"
        elif id == 0:
            return "Flashlight"
        elif id == 1:
            return "Mirror"
        elif id == 2:
            return "Colored Glass"
        elif id == 3:
            return "Prism"
        elif id == 4:
            return "Drawing Mode"
        elif id == 5:
            return "Lens"
        elif id == 6:
            return "Corridor"
        else:
            return "Unknown"

    def load_settings(self):
        self.width = self.game.width
        self.height = self.game.height // 10
        self.position = self.game.settings['HOTBAR_POSITION']

        if self.position == 'bottom':
            self.rect = pygame.Rect(0, self.height * 10 - self.height, self.width, self.height)
        elif self.position == 'left':
            self.rect = pygame.Rect(0, 0, self.width // 10, self.height * 10)
        elif self.position == 'right':
            self.rect = pygame.Rect(self.width - self.width // 10, 0, self.width // 10, self.height * 10)
        elif self.position == 'top':
            self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.buttons = [button.Button(self.game, x, tooltip_text=self.tooltip_list(x)) for x in
                        range(self.button_min, self.button_max)]  # creates buttons
