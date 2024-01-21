import cProfile
from classes import game, sounds
from gui import gui_main as gui
import pygame
import settingsSetup
from gui import startscreen as ss

def main():
    settings = settingsSetup.start()
    width = settings['WIDTH']
    height = settings['HEIGHT']

    position = settings['HOTBAR_POSITION']

    programIcon = pygame.image.load('images/torch_icon.png')

    pygame.display.set_icon(programIcon)

    startscreen = ss.StartScreen(width, height)

    # sounds.soundtrack()

    game_instance = game.Game()
    # light1=light.Light(game,[[0,0],[100,10],[200,300]],(255,255,255))
    GUI = gui.GUI(game_instance)
    # print(pygame.display.Info())
    game_instance.loop()

if __name__ == "__main__":
    cProfile.run("main()", sort="tottime")
