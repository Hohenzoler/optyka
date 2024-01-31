class ButtonAnimation:
    def __init__(self, button, target_position):
        self.button = button
        self.target_position = target_position

    def animate(self):
        self.button.rect.y += (self.target_position - self.button.rect.y) * 0.1
        self.button.textRect.center = (self.button.rect[0] + (self.button.rect[2] // 2), self.button.rect[1] + (self.button.rect[3] // 2))