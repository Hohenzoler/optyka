
import pygame
from gui import gui_main as gui
from gui import settings_screen
from classes import gameobjects
import settingsSetup
from classes import fps
from classes import bin, images
from classes.achievements import Achievements

class Game:
    """
    The main game class that handles the game loop, events, rendering and settings.
    """
    def __init__(self):
        """
        Initializes the game with settings, pygame, objects, and other necessary attributes.
        """
        self.settings = settingsSetup.load_settings()  # Load game settings
        self.width = self.settings['WIDTH']  # Game width
        self.height = self.settings['HEIGHT']  # Game height
        self.font = pygame.font.Font(None, self.height//20)  # Font for displaying FPS
        self.objects = []  # List of game objects
        pygame.init()  # Initialize pygame
        # Set up the game display based on settings
        if self.settings['FULLSCREEN'] == 'ON':
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=0)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), vsync=0)
        self.run = True  # Game loop control
        self.fps = fps.return_fps()  # Frames per second
        self.tick = int((1 / self.fps) * 1000)  # Time per frame in milliseconds
        self.mousepos = None  # Mouse position which will be updated every time the left mouse button is clicked
        self.rightclickedmousepos = None  # Right click mouse position
        self.r = False  # Used for mouse wheel events
        self.current_flashlight = None  # Current flashlight object
        self.mode = 'default'  # Current game mode
        self.executed_command = 'default'  # Last executed command
        self.clock = pygame.time.Clock()  # Pygame clock for controlling FPS
        pygame.mouse.set_visible(False)  # Hide the default mouse cursor
        self.cursor_img = images.bad_coursor  # Custom cursor image
        self.cursor_img_rect = self.cursor_img.get_rect()  # Rectangle for the custom cursor image
        self.achievements = Achievements()  # Achievements object

        self.p = False #used for properties windows for gameobjects

    def events(self):
        """
        Handles all the pygame events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            if self.mode == 'default':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousepos = event.pos  # when the left button is clicked the position is saved to self.mousepos
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.rightclickedmousepos = event.pos
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.r = 10
                    if event.y < 0:
                        self.r = -10
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.p = True
            elif self.mode == 'settings':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for object in self.objects:
                        if type(object) == settings_screen.Settings_screen:
                            object.checkevent(event.pos)

    def update(self):
        """
        Updates the game display and controls the game FPS.
        """
        pygame.display.update()
        self.clock.tick(self.fps)

    def render(self):
        """
        Renders all the game objects and the custom cursor.
        """
        if self.mode == 'default':
            sorted_objects = sorted(self.objects, key=lambda obj: getattr(obj, 'layer', 0))
            for object in sorted_objects:
                if type(self.mousepos) is tuple:
                    if type(object) is gui.GUI:
                        object.checkifclicked(self.mousepos)
                    if issubclass(type(object), gameobjects.GameObject):
                        object.checkifclicked(self.mousepos)
                if type(self.rightclickedmousepos) is tuple:
                    if issubclass(type(object), gameobjects.GameObject):
                        object.selected(self.rightclickedmousepos)

                object.render()
                if type(object) != bin.Bin:
                    for bin_2 in self.objects:
                        if type(bin_2) == bin.Bin:
                            bin_2.checkCollision(object)
                            break
        elif self.mode == 'settings':
            if self.executed_command != 'settings':
                self.settings_screen = settings_screen.Settings_screen(self)
                self.settings_screen.render()
                self.executed_command = 'settings'
            else:
                self.settings_screen.render()
        elif self.mode == 'load_new_settings':
            self.objects.remove(self.settings_screen)
            self.settings_screen = None
            self.mode = 'default'
            self.settings = settingsSetup.load_settings()
            self.width = self.settings['WIDTH']
            self.height = self.settings['HEIGHT']
            if self.settings['FULLSCREEN'] == 'ON':
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((self.width, self.height))
            for object in self.objects:
                if type(object) == gui.GUI or type(object) == bin.Bin:
                    object.load_settings()
            self.executed_command = 'default'
        self.cursor_img_rect.center = pygame.mouse.get_pos()  # update position
        self.screen.blit(self.cursor_img, self.cursor_img_rect)  # draw the cursor
        self.displayFPS()

    def background(self):
        """
        Fills the game display with black color.
        """
        self.screen.fill((0, 0, 0))

    def displayFPS(self):
        """
        Displays the current FPS on the game display.
        """
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", True, "white")
        self.screen.blit(fps_text, (10, 10))

    def loop(self):
        """
        The main game loop.
        """
        while self.run:
            self.background()
            self.render()
            self.update()
            self.mousepos = None  # resets self.mouspos
            self.rightclickedmousepos = None
            self.events()
