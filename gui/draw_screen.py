import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Polygon Creator")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Point list to store the vertices of the polygon
point_list = []


# Function to draw the polygon on the screen
def draw_polygon(points):
    pygame.draw.polygon(screen, red, points)


# Function to display the confirmation screen
def confirm_screen(points):
    confirm_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    draw_polygon(points)
    confirm_surface.blit(screen, (0, 0))

    font = pygame.font.Font(None, 36)
    text = font.render("Polygon Created!", True, white)
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    confirm_surface.blit(text, text_rect)

    text = font.render("Press Enter to continue", True, white)
    text_rect = text.get_rect(center=(width // 2, height // 2 + 50))
    confirm_surface.blit(text, text_rect)

    screen.blit(confirm_surface, (0, 0))
    pygame.display.flip()


# Main game loop
running = True
drawing = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if drawing:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point_list.append(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                drawing = False

    screen.fill(black)

    if drawing:
        # Draw points
        for point in point_list:
            pygame.draw.circle(screen, white, point, 5)

        # Draw lines between points
        if len(point_list) > 1:
            pygame.draw.lines(screen, white, False, point_list, 2)

    else:
        # Confirmation screen
        confirm_screen(point_list)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
