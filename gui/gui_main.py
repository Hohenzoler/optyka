import pygame
from gui import button
from classes import bin, slider


class GUI:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height // 10
        self.position = self.game.settings['HOTBAR_POSITION']

        self.red_slider = slider.Slider(50, 50, 200, 20, 0, 255, 255)
        self.green_slider = slider.Slider(50, 100, 200, 20, 0, 255, 255)
        self.blue_slider = slider.Slider(50, 150, 200, 20, 0, 255, 255)

        if self.position == 'bottom':
            self.rect = pygame.Rect(0, self.height*10 - self.height, self.width, self.height)
        elif self.position == 'left':
            self.rect = pygame.Rect(0, 0, self.width//10, self.height*10)
        elif self.position == 'right':
            self.rect = pygame.Rect(self.width - self.width//10, 0, self.width//10, self.height*10)
        elif self.position == 'top':
            self.rect = pygame.Rect(0, 0, self.width, self.height)


        self.layer = 2  # Assign a higher layer value to GUI to ensure it's rendered on top
        self.game.objects.append(self)
        self.f = None

        self.bin = bin.Bin(self.game)

        self.buttons = [button.Button(self.game, x) for x in range(-2, 6)] #creates buttons


    def render(self):
        pygame.draw.rect(self.game.screen, (100, 100, 100), self.rect)
        for button in self.buttons: #renders buttons
            button.render()
        self.red_slider.render(self.game.screen)
        self.green_slider.render(self.game.screen)
        self.blue_slider.render(self.game.screen)

    def checkifclicked(self, mousepos):
        for button in self.buttons:
            button.checkifclicked(mousepos)

        if self.red_slider.check_if_clicked(mousepos) or self.green_slider.check_if_clicked(
                mousepos) or self.blue_slider.check_if_clicked(mousepos):
            r = self.red_slider.get_value()
            g = self.green_slider.get_value()
            b = self.blue_slider.get_value()
            # Assuming the light color is stored in self.game.current_flashlight.color
            if self.game.current_flashlight:
                self.game.current_flashlight.color = (r, g, b)


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

        self.buttons = [button.Button(self.game, x) for x in range(-2, 5)] #creates buttons