import pygame
from classes import font


class Popup:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen

    def rarity_color(self, rarity):
        if rarity == 'common':
            color = (163, 163, 163)
        elif rarity == 'uncommon':
            color = (10, 145, 6)
        elif rarity == 'rare':
            color = (15, 109, 163)
        elif rarity == 'epic':
            color = (97, 37, 143)
        elif rarity == 'legendary':
            color = (222, 182, 24)
        else:
            color = (50, 50, 50)
        return color

    def render_achievement(self, achievement, rarity, x_offset, y_offset):
        self.smol_font = pygame.font.Font(font.Font, 16)
        self.normal_font = pygame.font.Font(font.Font, 22)
        self.rarity = rarity
        achievement_name = achievement
        text_color = (255, 255, 255)

        color = self.rarity_color(self.rarity)

        rect_width = self.width // 2 - 100
        rect_height = 40

        textRect = pygame.Rect(x_offset, y_offset, rect_width, rect_height)

        # Calculate the center of the rectangle
        center_x = x_offset + rect_width // 2
        center_y = y_offset + rect_height // 2

        pygame.draw.rect(self.game.screen, color, textRect.inflate(10, 10), 0, 5)

        unlocked_text_surface = self.normal_font.render("Achievement Unlocked", True, text_color)
        unlocked_text_rect = unlocked_text_surface.get_rect(center=(center_x, center_y - 10))
        self.game.screen.blit(unlocked_text_surface, unlocked_text_rect)

        text_surface = self.smol_font.render(f"{achievement_name}", True, text_color)
        text_surface_rect = text_surface.get_rect(center=(center_x, center_y + 12))
        self.game.screen.blit(text_surface, text_surface_rect)

        return y_offset + rect_height + 20
