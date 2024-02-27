import cProfile
import logging
import tkinter
from datetime import datetime
from classes import game
from gui import gui_main as gui
import pygame
import settingsSetup
from screens import startscreen as ss
import os

# Create a "logs" folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("saves"):
    os.makedirs("saves")

if not os.path.exists("presets"):
    os.makedirs("presets")

# Set up the logging configuration
log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


version = '1.0 pre-release WOOOOO :D!'

def new_game(save, preset):
    try:
        settings = settingsSetup.start()
        width = settings['WIDTH']
        height = settings['HEIGHT']

        position = settings['HOTBAR_POSITION']

        programIcon = pygame.image.load('images/torch_icon.png')
        pygame.display.set_icon(programIcon)

        game_instance = game.Game(save, preset)
        GUI = gui.GUI(game_instance)
        game_instance.loop()

    except Exception as e:
        # Log any unhandled exceptions
        logging.error(e, exc_info=True)
        raise

if __name__ == "__main__":
    while True:
        try:
            startscreen = ss.StartScreen(version)
            new_game(startscreen.save_to_load, startscreen.preset)
        except Exception as e:
            print(e)
            raise
            # logging.error(e, exc_info=True)
            # tkinter.messagebox.showerror("Error", "An error occurred. Please check the logs for more information.")
            # raise
            break
#
