import pygame


def selected_sound():
    selected_sound = pygame.mixer.Sound('sounds/select.wav')
    selected_sound.play()
    pass


def placed_sound():
    placed_sound = pygame.mixer.Sound('sounds/place.wav')
    placed_sound.play()
    pass


def clicked_sound():
    clicked_sound = pygame.mixer.Sound('sounds/select.wav')
    clicked_sound.play()
    pass

def laser_sound():
    laser_sound = pygame.mixer.Sound('sounds/place.wav')
    laser_sound.play()
    pass

def destroy_sound():
    destroy_sound = pygame.mixer.Sound('sounds/explosion.wav')
    destroy_sound.play()
    pass

def soundtrack():
    pygame.mixer.music.load('sounds/mc.mp3')
    pygame.mixer.music.play(-1)
    pass

if __name__ == '__main__':
    # print("why are you running this file?")
   pass