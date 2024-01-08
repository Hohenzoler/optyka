import pygame


def selected_sound():
    selected_sound = pygame.mixer.Sound('sounds/selected.wav')
    selected_sound.play()


def placed_sound():
    placed_sound = pygame.mixer.Sound('sounds/place.wav')
    placed_sound.play()


def clicked_sound():
    clicked_sound = pygame.mixer.Sound('sounds/goofy_ahh.wav')
    clicked_sound.play()

def laser_sound():
    laser_sound = pygame.mixer.Sound('sounds/laser_sound.wav')
    laser_sound.play()

if __name__ == '__main__':
    print("why are you running this file?")