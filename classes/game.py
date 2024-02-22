import json
import random
import os
import pygame
import math
# from math import *
from pygame import *
from gui import gui_main as gui1
from gui.gui_main import GUI
from screens import settings_screen
import settingsSetup
from classes import fps
from classes import bin, images, gameobjects
from classes.achievements import Achievements
from classes import parkinson as particles
from classes.font import Font
import time
from datetime import datetime
import functions
import gui
from gui.polygonDrawing import polygonDrawing
from classes import popup
from classes import saveTK, mixer_c


isDrawingModeOn = False

class Game:
    """
    The main game class that handles the game loop, events, rendering and settings.
    """
    def __init__(self, save, preset):
        """
        Initializes the game with settings, pygame, objects, and other necessary attributes.
        """
        self.save_to_load = save
        self.settings = settingsSetup.load_settings()  # Load game settings
        self.width = self.settings['WIDTH']  # Game width
        self.height = self.settings['HEIGHT']  # Game height
        self.font = pygame.font.Font(Font, self.height//20)  # Font for displaying FPS
        self.objects = []  # List of game objects
        pygame.init()  # Initialize pygame
        # Set up the game display based on settings
        if self.settings['FULLSCREEN'] == 'ON':
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=0)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), vsync=0)
        self.isDrawingModeOn = False


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
        self.cursor_img = images.bad_coursor  # Custom cursor image
        self.cursor_img_rect = self.cursor_img.get_rect()  # Rectangle for the custom cursor image
        self.pen_img = images.pen
        self.pen_img_rect = self.pen_img.get_rect()
        self.achievements = Achievements(self)  # Achievements object

        self.mixer = mixer_c.Mixer(self.settings)

        self.achievements.handle_achievement_unlocked("here is your first achievement ;)")

        self.p = False #used for properties windows for gameobjects
        self.r_key = False # used for resizing objects

        self.selected_object = None

        self.cursor_particle_system = particles.UnityParticleSystem()

        self.cached_mousepos = None

        self.surface_num = 12 # IMPORTANT lower numbers = higher fps, higher numbers = better quality
        self.surfaces = [pygame.Surface((self.width, self.height), pygame.SRCALPHA) for _ in range(self.surface_num)]
        for surface in self.surfaces:
            surface.set_alpha(40)

        self.surface_rays = {i : [] for i in range(self.surface_num)}

        self.save = False
        self.save_title = None
        self.preset = preset
        self.cancel = False

        self.background_color = (0, 0, 0)

        self.last_scroll_time = time.time()

        self.popup_start_time = None
        self.popup = False
        self.currentAchievementName = None

        self.polygonDrawing = polygonDrawing()


    def create_cursor_particles(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.cursor_particle_system.add_particle(
            mouse_x, mouse_y,
            random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5),
            200, random.randint(1, 2),
            random.randint(200, 255), random.randint(200, 255), random.randint(200, 255),
            150, 'square'
        )

    def create_clicked_particles(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i in range(20):
            self.cursor_particle_system.add_particle(
                mouse_x, mouse_y,
                random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5),
                50, random.randint(2, 3),
                random.randint(200, 255), random.randint(200, 255), random.randint(200, 255),
                200, 'circle'
            )

    def return_fps(self):
        return self.displayFPS()

    def scrolling(self, eventos):
        current_time = time.time()
        time_difference = current_time - self.last_scroll_time
        self.last_scroll_time = current_time
        if round(time_difference, 2) != 0:
            if eventos.y > 0:
                if time_difference > 1:
                    self.r = 1
                else:
                    self.r = round(1 / (time_difference * 9), 2)
            if eventos.y < 0:
                if time_difference > 1:
                    self.r = -1
                else:
                    self.r = round(-1 / (time_difference * 9), 2)

    def events(self):
        """
        Handles all the pygame events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game()
                if self.cancel == False:
                    pygame.quit()
                    quit()


            if self.mode == 'default':
                points = polygonDrawing.returnPolygonPoints(self.polygonDrawing)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousepos = event.pos  # when the left button is clicked the position is saved to self.mousepos
                    for object in self.objects:
                        if type(object) in (gameobjects.GameObject, gameobjects.Mirror, gameobjects.Lens, gameobjects.Flashlight, gameobjects.Prism, gameobjects.CustomPolygon, gameobjects.ColoredGlass) and object.resizing:
                            if object.resize_on is False:
                                for idx, rect in enumerate(object.resize_rects):
                                    if rect.collidepoint(self.mousepos):
                                        object.resize_on = True
                                        object.resize_point_index = idx
                                        resize_point = object.points[idx]
                                        for index, point in enumerate(object.points):
                                            if point[0] == resize_point[0] and point != resize_point:
                                                object.x_resize_index = index

                                            elif point[1] == resize_point[1] and point != resize_point:
                                                object.y_resize_index = index
                                                pygame.draw.circle(self.screen, (0, 255, 0), point, 5)
                                            elif point != resize_point:
                                                object.static_point_index = index
                                                pygame.draw.circle(self.screen, (255, 0, 0), point, 5)
                            else:
                                object.resize_on = False
                    if self.isDrawingModeOn:
                        polygonDrawing.addPoint(self.polygonDrawing, self.mousepos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.create_clicked_particles()
                    if event.button == 3:
                        self.rightclickedmousepos = event.pos
                        if self.isDrawingModeOn:
                            for i in range(len(points)):
                                distance = ((points[i][0] - 5 - self.rightclickedmousepos[0]) ** 2 + (points[i][1] - self.rightclickedmousepos[1]) ** 2 ) ** 0.5
                                if distance < 10:
                                    pass
                                print(distance)
                if event.type == pygame.MOUSEWHEEL:
                    self.scrolling(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.p = True
                    if event.key == pygame.K_r and self.selected_object is not None:
                        self.r_key = True
                        self.selected_object.selected(pygame.mouse.get_pos())
                    elif event.key == 13 and self.isDrawingModeOn:
                        polygonDrawing.createPolygon(self.polygonDrawing, self)
                        polygonDrawing.clearPoints(self.polygonDrawing)
                        global isDrawingModeOn
                        isDrawingModeOn = False
                        self.achievements.handle_achievement_unlocked("topopisy")
                    elif event.key == pygame.K_BACKSPACE and len(points) > 0:
                        polygonDrawing.popapoint(self.polygonDrawing)



            elif self.mode == 'settings':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for object in self.objects:
                        if isinstance(object, settings_screen.Settings_screen):
                            object.checkevent(event.pos)

    def update(self):
        """
        Updates the game display and controls the game FPS.
        """
        pygame.display.update()
        self.clock.tick(self.fps)
        if isDrawingModeOn:
            self.isDrawingModeOn = True
        else:
            self.isDrawingModeOn = False

    def render_particles(self):
        """
        Renders all the game objects and the custom cursor.
        """
        if self.cached_mousepos != pygame.mouse.get_pos():
            self.create_cursor_particles()

        self.cached_mousepos = pygame.mouse.get_pos()

        self.cursor_particle_system.update()
        self.cursor_particle_system.draw(self.screen)

    def render(self):
        """
        Renders all the game objects and the custom cursor.
        """

        pygame.mouse.set_visible(False)  # Hide the default mouse cursor

        self.render_particles()

        if self.mode == 'default':
            if self.settings['HD_Flashlight'] == 'ON':
                for surface in self.surfaces:
                    surface.fill((0, 0, 0, 0))
                #self.surfaces = [surface.copy() for surface in self.default_surfaces]

                for surface_num, rays in self.surface_rays.items():
                    if surface_num > self.surface_num -1:
                        break
                    for ray in rays:
                        functions.draw_thick_line(self.surfaces[surface_num], int(ray.start_point[0]), int(ray.start_point[1]),
                                             int(ray.end_point[0]), int(ray.end_point[1]), ray.color, 5)
                    self.screen.blit(self.surfaces[surface_num], (0, 0))

                self.surface_rays = {i: [] for i in range(self.surface_num)}

            sorted_objects = sorted(self.objects, key=lambda obj: getattr(obj, 'layer', 0))
            for object in sorted_objects:
                if type(self.mousepos) is tuple:
                    if type(object) is gui1.GUI:
                        object.checkifclicked(self.mousepos)
                    if isinstance(object, gameobjects.GameObject):
                        object.checkifclicked(self.mousepos)
                if type(self.rightclickedmousepos) is tuple:
                    if isinstance(object, gameobjects.GameObject):
                        object.selected(self.rightclickedmousepos)


                object.render()
                if type(object) != bin.Bin:
                    for bin_2 in self.objects:
                        if type(bin_2) == bin.Bin:
                            bin_2.checkCollision(object)
                            break
            # if self.isDrawingModeOn:
            #     optyka.gui.polygonDrawing.renderDots()
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
            self.mixer = mixer_c.Mixer(self.settings)
            if self.settings['FULLSCREEN'] == 'ON':
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((self.width, self.height))
            for object in self.objects:
                if type(object) == gui1.GUI or type(object) == bin.Bin:
                    object.load_settings()
            self.executed_command = 'default'

        self.cursor_img_rect.center = pygame.mouse.get_pos()  # update position
        if isDrawingModeOn:

            points = polygonDrawing.returnPolygonPoints(self.polygonDrawing)
            self.screen.blit(self.pen_img, self.cursor_img_rect)
            for i in range(len(points)):
                pygame.draw.circle(self.screen, (200, 0, 0), points[i], 5)
            if len(points) >= 2:
                pygame.draw.lines(self.screen, (255, 255, 255), True, points)
        else:
            self.screen.blit(self.cursor_img, self.cursor_img_rect)  # draw the cursor
        self.displayFPS()
        self.displayClock()
        if self.popup == True:
            if time.time() - self.popup_start_time >= 5:
                self.popup = False
                self.popup_start_time = None
                self.currentAchievementName = None
                self.currentAchievementRarity = None
            else:
                popup.Popup.render_achievement(popup.Popup(self), self.currentAchievementName, self.currentAchievementRarity, 50, 100)
                print(self.currentAchievementName)



    def background(self):
        # Use the background color attribute to fill the game display
        self.screen.fill(self.background_color)

    def displayFPS(self):
        """
        Displays the current FPS on the game display.
        """
        if self.settings['HOTBAR_POSITION'] != 'top':
            self.y = 12.5
        else:
            self.y = self.height // 7

        if self.settings['HOTBAR_POSITION'] != 'left':
            self.x = 12.5
        else:
            self.x = self.width // 9
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", True, "white")
        self.screen.blit(fps_text, (self.x, self.y))
        return fps

    def displayClock(self):
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        current_second = current_time.tm_sec
        if current_hour < 10:
            current_hour = f"0{current_hour}"
        if current_minute < 10:
            current_minute = f"0{current_minute}"
        if current_second < 10:
            current_second = f"0{current_second}"
        time_text = self.font.render(f"{current_hour}:{current_minute}:{current_second}", True, "white")

        if self.settings['HOTBAR_POSITION'] != 'top':
            self.y = 12.5
        else:
            self.y = self.height // 7

        if self.settings['HOTBAR_POSITION'] != 'right':
            self.x = 0
        else:
            self.x = self.width // 10

        self.screen.blit(time_text, (self.width-(time_text.get_rect().width*1.1)-self.x, self.y))
        return time_text

    def achievement_popup(self, achname, rarity):
        self.popup = True
        self.currentAchievementName = achname
        self.currentAchievementRarity = rarity
        self.popup_start_time = time.time()

    def loop(self):
        screen = self.screen
        """
        The main game loop.
        """
        while self.run:
            self.background()
            self.render()
            self.update()
            self.mousepos = None  # resets self.mouspos
            self.rightclickedmousepos = None
            self.p = False
            self.r_key = False
            self.events()
            self.achievements.fps_achievements()
            if self.save_to_load != None:
                self.load()
                self.save_to_load = None



    def load(self):
        if not self.preset:
            try:
                with open(f"saves/{self.save_to_load}.json", 'r') as f:
                    save = json.load(f)
                    f.close()
            except:
                save = {}
        else:
            try:
                with open(f"presets/{self.save_to_load}.json", 'r') as f:
                    save = json.load(f)
                    f.close()
            except:
                save = {}
        self.save_title = self.save_to_load
        for parameters in save:
            if not isinstance(parameters, dict):
                continue

            mousepos = (500, 500)
            if parameters['class'] == "Flashlight":
                obj = gameobjects.Flashlight(self, [(mousepos[0], mousepos[1]), (mousepos[0] + 200, mousepos[1]), (mousepos[0] + 200, mousepos[1] + 100), (mousepos[0], mousepos[1] + 100)], (255, 255, 255), 0, 0.4, 0.5, image=images.torch)

            elif parameters['class'] == "Mirror":
                obj = gameobjects.Mirror(self, [(mousepos[0] - 100, mousepos[1] - 50), (mousepos[0] + 100, mousepos[1] - 50), (mousepos[0] + 100, mousepos[1] + 50), (mousepos[0] - 100, mousepos[1] + 50)], (255, 0, 0), 0, 0.9, 0.5, textureName='wood')

            elif parameters['class'] == "ColoredGlass":
                obj = gameobjects.ColoredGlass(self, [(mousepos[0] - 10, mousepos[1] - 50), (mousepos[0] + 10, mousepos[1] - 50), (mousepos[0] + 10, mousepos[1] + 50), (mousepos[0] - 10, mousepos[1] + 50)], (0, 255, 0), 0, 0.4, 0.5)

            elif parameters['class'] == "Prism":
                obj = gameobjects.Prism(self, [(mousepos[0] - 50, mousepos[1]), (mousepos[0], mousepos[1] - 100), (mousepos[0] + 50, mousepos[1])], None, 0, 1, 1)

            elif parameters['class'] == "Lens":
                obj = gameobjects.Lens(self, [(mousepos[0] - 100, mousepos[1] - 100), (mousepos[0], mousepos[1] - 100), (mousepos[0], mousepos[1] + 100), (mousepos[0] - 100, mousepos[1] + 100)], (64, 137, 189), 0, 0, 140, 0, 0.5)

            # elif parameters['class'] == ""

            obj.parameters = parameters
            obj.change_parameters('not')
            if parameters['class'] == "Prism":
                self.objects.insert(3, obj)
            else:
                self.objects.append(obj)
    def generate_save(self):
        self.save_obj = []

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_obj.append(formatted_time)

        for object in self.objects:
            if issubclass(type(object), gameobjects.GameObject):
                object.find_parameters()
                object.parameters['class'] = object.__class__.__name__
                self.save_obj.append(object.parameters)
                print(object.parameters)
        if not os.path.exists("saves"):
            os.makedirs("saves")


    def save_to_file(self):
        if os.path.exists(f'saves/{self.save_title}'):
            old_save = settingsSetup.load_settings(f'saves/{self.save_title}.json')
            new_save = old_save.update(self.save_obj)
            settingsSetup.writesettingstofile(new_save, 2, f'saves/{self.save_title}.json')
        else:
            settingsSetup.writesettingstofile(self.save_obj, 2, f'saves/{self.save_title}.json')

    def save_game(self):
        if not self.preset:
            self.generate_save()
            if len(self.objects) > 3:
                if self.save_title != None:
                    prev_save_data = settingsSetup.load_settings(f'saves/{self.save_title}.json')
                    if len(prev_save_data) > 1:
                        if prev_save_data[1:] != self.save_obj[1:]:
                            pygame.mouse.set_visible(True)
                            a = saveTK.Save(self)
                    else:
                        pygame.mouse.set_visible(True)
                        a = saveTK.Save(self)
                else:
                    pygame.mouse.set_visible(True)
                    a = saveTK.Save(self)

            elif len(self.objects) == 3 and self.save_title != None:
                prev_save_data = settingsSetup.load_settings(f'saves/{self.save_title}.json')
                if len(prev_save_data) != 1:
                    pygame.mouse.set_visible(True)
                    a = saveTK.Save(self)
            elif len(self.objects) == 3:
                pass
            else:
                pygame.mouse.set_visible(True)
                a = saveTK.Save(self)
        if self.cancel == False:
            self.run = False
        self.cancel = False


