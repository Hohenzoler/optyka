import pygame


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.slider_pos = (x + (initial_val - min_val) / (max_val - min_val) * width, y)

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.slider_pos[0]-10), int(self.slider_pos[1])+10), 10)

    def check_if_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.slider_pos = (pos[0], self.slider_pos[1])
            self.val = self.min_val + (self.slider_pos[0] - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
            return True
        return False

    def get_value(self):
        return int(self.val)