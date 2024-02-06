import pygame
import sqlite3
import classes.font
from classes import sounds

class AchievementsScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 24)  # Adjust the font size as needed
        self.achievements = []
        self.load_achievements()

    def load_achievements(self):
        conn = sqlite3.connect('achievements.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM achievements")
        self.achievements = cursor.fetchall()
        conn.close()

    def render(self):
        font = pygame.font.Font(classes.font.Font, self.game.width // 30)

        text = font.render('Achievements', True, (255, 255, 255))

        text_rect = text.get_rect()

        text_rect.centerx = self.game.screen.get_rect().centerx
        self.game.screen.blit(text, text_rect)
        text_rect.y = 10
        y_offset = 100
        for achievement in self.achievements:
            achievement_name, unlocked, rarity = achievement
            color = (0, 255, 0) if unlocked else (255, 0, 0)
            text_surface = self.font.render(f"{achievement_name} - {rarity}", True, color)
            self.game.screen.blit(text_surface, (50, y_offset))
            y_offset += 30

class Button:
    def __init__(self, game, text, x, y, width, height, action):
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.font = pygame.font.Font(None, 24)

    def render(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, (0, 200, 0))
        self.game.screen.blit(text_surface, (self.x + 10, self.y + 10))

    def is_clicked(self, pos):
        sounds.clicked_sound()
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height