import pygame
from classes import gameobjects as go
from classes import parkinson as particles, achievements, color_picker
import random
from classes import light


class Bin:
    """
    This class represents a Bin in the game. It has methods to check collision with game objects,
    render itself and load settings from the game settings.
    """

    def __init__(self, game):
        """
        Initializes the Bin object.

        Args:
            game (Game): The game object that this Bin is part of.
        """
        self.particle_system = particles.UnityParticleSystem()
        self.game = game
        self.x = self.game.width - 150
        self.y = self.game.height - 200

        self.rect = pygame.Rect(self.x, self.y, 100, 100)

        self.particle_center_x = self.x + 88
        self.particle_center_y = self.y + 60

        self.game.objects.append(self)

        self.bin_img = pygame.image.load("images/trash1.png")

        self.load_parameters()

        # self.game.objects.append(self)

        self.achievements = game.achievements

    def checkCollision(self, obj):
        """
        Checks if the Bin has collided with a game object.

        Args:
            obj (GameObject): The game object to check collision with.
        """
        if type(obj) != light.Light:
            if obj.rect.colliderect(self.rect) and isinstance(obj, go.GameObject):
                if obj.color != None:
                    rgb = obj.color
                else:
                    rgb = (255, 255, 255)
                for i in range(random.randint(60, 300)):
                    self.particle_system.add_particle(self.particle_center_x, self.particle_center_y,
                                                      random.uniform(-1.5, 1.5) * obj.scale_factor,
                                                      random.uniform(-1.5, 1.5) * obj.scale_factor, 220,
                                                      random.randint(1, 7) * obj.scale_factor,
                                                      random.randint(rgb[0] // 2, rgb[0]),
                                                      random.randint(rgb[1] // 2, rgb[1]),
                                                      random.randint(rgb[2] // 2, rgb[2]), 220,
                                                      random.choice(['square', 'circle', 'triangle']))
                self.game.objects.remove(obj)
                self.game.selected_object = None
                self.game.mixer.destroy_sound()
                achievements.Achievements.handle_achievement_unlocked(self.achievements, "kaboom")

    def render(self):
        """
        Renders the Bin on the game screen.
        """
        self.game.screen.blit(self.bin_img, self.rect)
        self.particle_system.update()
        self.particle_system.draw(self.game.screen)

    def load_settings(self):
        """
        Loads the settings from the game settings.
        """
        self.load_parameters()

    def load_parameters(self):
        """
        Loads the parameters from the game settings.
        """
        settings = self.game.settings

        self.x = self.game.width - self.game.width // 12
        self.y = self.game.height - self.game.height // 4.5

        if settings['HOTBAR_POSITION'] != 'bottom':
            self.y = self.game.height - self.game.height // 7
            if settings['HOTBAR_POSITION'] != 'right':
                self.x = self.game.width - self.game.width // 10

            else:
                self.x = self.game.width - self.game.width // 5

        self.rect_w = self.game.width // 17
        self.rect_h = self.game.height // 11

        self.bin_img = pygame.transform.scale(self.bin_img, (self.rect_w, self.rect_h))

        self.rect = pygame.Rect(self.x, self.y, self.rect_w, self.rect_h)

        self.particle_center_x = self.x + self.rect_w // 2
        self.particle_center_y = self.y + self.rect_h // 2
