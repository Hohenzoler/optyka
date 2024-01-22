import cProfile
import logging
import os
from datetime import datetime
from classes import game, sounds
from gui import gui_main as gui
import pygame
import settingsSetup
from gui import startscreen as ss

# Create a "logs" folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Set up the logging configuration
log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    try:
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

    except Exception as e:
        # Log any unhandled exceptions
        logging.error(e, exc_info=True)
        raise

if __name__ == "__main__":
    main()
    # Use cProfile to profile your code
    # cProfile.run("main()", sort="tottime")
