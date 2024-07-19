import pygame
import random

class Mixer:
    def __init__(self, settings):
        self.mastervolume = settings['MASTER_VOLUME']
        self.soundtrackvolume = settings['SOUNDTRACK_VOLUME'] * self.mastervolume
        self.objectvolume = settings["OBJECT_VOLUME"] * self.mastervolume
        self.actionvolume = settings["ACTION_VOLUME"] * self.mastervolume
        self.achievementvolume = settings["ACHIEVEMENT_VOLUME"] * self.mastervolume

    def selected_sound(self):
        selected_sound = pygame.mixer.Sound('sounds/metsej/metsej_1.wav')
        selected_sound.set_volume(self.actionvolume)
        selected_sound.play()
        pass

    def placed_sound(self):
        placed_sound = pygame.mixer.Sound('sounds/metsej/metsej_2.wav')
        placed_sound.set_volume(self.actionvolume)
        placed_sound.play()
        pass

    def clicked_sound(self):
        clicked_sound = pygame.mixer.Sound('sounds/metsej/metsej_1.wav')
        clicked_sound.set_volume(self.actionvolume)
        clicked_sound.play()
        pass

    def laser_sound(self):
        laser_sound = pygame.mixer.Sound('sounds/metsej/metsej_2.wav')
        laser_sound.set_volume(self.objectvolume)
        laser_sound.play()
        pass

    def destroy_sound(self):
        destroy_sound = pygame.mixer.Sound('sounds/explosion.wav')
        destroy_sound.set_volume(self.objectvolume)
        destroy_sound.play()
        pass

    def achievement_sound(self):
        achievement_sound = pygame.mixer.Sound('sounds/metsej/metsej_3.wav')
        achievement_sound.set_volume(self.achievementvolume)
        achievement_sound.play()
        pass

    def soundtrack(self):
        x = random.randint(1, 1000)
        print(x)
        if x == 69 or x == 420:
            pygame.mixer.music.load('sounds/jews.mp3')
        else:
            pygame.mixer.music.load('sounds/mc.mp3')
        pygame.mixer.music.set_volume(self.soundtrackvolume)
        pygame.mixer.music.play(-1)
        pass
