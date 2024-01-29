import os
import pygame
from pygame.locals import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 500
BUTTON_HEIGHT = 80
CONTAINER_WIDTH = 600
CONTAINER_HEIGHT = 400
SCROLL_SPEED = 30
NUM_BUTTONS_DISPLAYED = 4
BUTTON_SPACING = 20  # Adjust the spacing between buttons

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World Selection Menu")

# Font
font = pygame.font.SysFont(None, 40)

# Directory containing world files
world_dir = "C:/Users/This PC/Documents/GitHub/optyka/saves"

# Get list of world files
world_files = [file for file in os.listdir(world_dir) if file.endswith('.json')]

# Determine if scrolling is needed
scrolling_needed = len(world_files) > NUM_BUTTONS_DISPLAYED

# Initial scroll position
scroll_offset = 0

class Button:
    def __init__(self, text, x, y, width, height, color=GRAY, outline_color=BLACK, outline_thickness=2):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.outline_color, self.rect, self.outline_thickness)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_visible(self, container_rect):
        return container_rect.contains(self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create initial buttons
buttons = []
for i in range(NUM_BUTTONS_DISPLAYED):
    if i < len(world_files):
        button = Button(world_files[i], (SCREEN_WIDTH - BUTTON_WIDTH ) // 2, (SCREEN_HEIGHT - CONTAINER_HEIGHT - 150) // 2 + i * (BUTTON_HEIGHT + BUTTON_SPACING) + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append(button)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4 and scrolling_needed:  # Scroll up
                if scroll_offset > 0:
                    scroll_offset -= 1
            elif event.button == 5 and scrolling_needed:  # Scroll down
                max_offset = max(0, len(world_files) - NUM_BUTTONS_DISPLAYED)
                if scroll_offset < max_offset:
                    scroll_offset += 1
            elif event.button == 1:  # Left mouse button
                # Check if any button is clicked
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        print(button.text)

    # Container
    container_rect = pygame.Rect((SCREEN_WIDTH - CONTAINER_WIDTH) // 2, (SCREEN_HEIGHT - CONTAINER_HEIGHT) // 2, CONTAINER_WIDTH, CONTAINER_HEIGHT)
    # pygame.draw.rect(screen, GRAY, container_rect)

    # Draw buttons
    for i, button in enumerate(buttons):
        button.rect.y = (SCREEN_HEIGHT - CONTAINER_HEIGHT) // 2 + i * (BUTTON_HEIGHT + BUTTON_SPACING) + BUTTON_SPACING
        if button.is_visible(container_rect):
            if i + scroll_offset < len(world_files):
                button.text = world_files[i + scroll_offset]
            button.draw(screen, font)

    # Update the display
    pygame.display.flip()

pygame.quit()
