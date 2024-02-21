import pygame


def selected_sound():
    selected_sound = pygame.mixer.Sound('sounds/metsej/metsej_1.wav')
    selected_sound.play()
    pass


def placed_sound():
    placed_sound = pygame.mixer.Sound('sounds/metsej/metsej_2.wav')
    placed_sound.play()
    pass


def clicked_sound():
    clicked_sound = pygame.mixer.Sound('sounds/metsej/metsej_1.wav')
    clicked_sound.play()
    pass

def laser_sound():
    laser_sound = pygame.mixer.Sound('sounds/metsej/metsej_2.wav')
    laser_sound.play()
    pass

def destroy_sound():
    destroy_sound = pygame.mixer.Sound('sounds/explosion.wav')
    destroy_sound.play()
    pass

def achievement_sound():
    achievement_sound = pygame.mixer.Sound('sounds/metsej/metsej_3.wav')
    achievement_sound.play()
    pass

def soundtrack():
    pygame.mixer.music.load('sounds/mc.mp3')
    pygame.mixer.music.play(-1)
    pass

if __name__ == '__main__':
    # print("why are you running this file?")
   pass