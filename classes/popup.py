import pygame


class Popup:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.screen = self.game.screen
        self.font = self.game.font


    def render_achievement(self, achievement, x_offset, y_offset):
        self.font = self.game.font
        achievement_name = achievement
        text_color = (255, 255, 255)
        text_surface = self.font.render(f"{achievement_name}", True, text_color)

        rect_width = self.width // 2 - 100
        rect_height = 50

        textRect = pygame.Rect(x_offset, y_offset, rect_width, rect_height)

        # Calculate the center of the rectangle
        center_x = x_offset + rect_width // 2
        center_y = y_offset + rect_height // 2

        text_surface_rect = text_surface.get_rect(center=(center_x, center_y))

        pygame.draw.rect(self.game.screen, (0, 0, 0), textRect.inflate(10, 10), 0, 5)
        self.game.screen.blit(text_surface, text_surface_rect)
        return y_offset + rect_height + 20

