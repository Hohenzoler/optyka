import pygame
import sys

class DropdownMenu:
    def __init__(self, screen, options, x, y, width, height, font, font_size, text_color, menu_color):
        self.screen = screen
        self.options = options
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.menu_color = menu_color
        self.expanded = False
        self.selected_option = None

    def draw(self):
        pygame.draw.rect(self.screen, self.menu_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.text_color, (self.x, self.y, self.width, self.height), 2)

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                pygame.draw.rect(self.screen, self.menu_color, option_rect)
                pygame.draw.rect(self.screen, self.text_color, option_rect, 2)

                option_text = self.font.render(option, True, self.text_color)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                self.screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dropdown_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                if dropdown_rect.collidepoint(event.pos):
                    self.expanded = not self.expanded
                else:
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = option
                            self.expanded = False
                            self.handle_button_click(option)

    def handle_button_click(self, option):
        print(f"Button clicked: {option}")

# Pygame setup
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dropdown Menu Example")

# Dropdown menu setup
options = ["Option 1", "Option 2", "Option 3"]
dropdown_menu = DropdownMenu(screen, options, 50, 50, 150, 30, None, 20, (255, 255, 255), (0, 0, 0))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        dropdown_menu.handle_event(event)

    screen.fill((255, 255, 255))
    dropdown_menu.draw()

    pygame.display.flip()
