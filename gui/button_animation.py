class ButtonAnimation:
    def __init__(self, button, target_position_x, target_position_y):
        self.button = button
        self.target_position_x = target_position_x
        self.target_position_y = target_position_y

    def animate(self):
        self.button.rect.x += (self.target_position_x - self.button.rect.x) * 0.1
        self.button.rect.y += (self.target_position_y - self.button.rect.y) * 0.1
        try:
            self.button.textRect.center = (self.button.rect[0] + (self.button.rect[2] // 2), self.button.rect[1] + (self.button.rect[3] // 2))
        except:
            pass