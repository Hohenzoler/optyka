import classes.game
import pygame
from classes import gameobjects, images
from classes.font import Font
from screens import music_settings


spiel = None
class Button:
    """
    This class represents a Button in the game.

    Attributes:
        game (object): The game object that this button is a part of.
        number (int): The number that identifies this button.
        screenheight (int): The height of the game screen.
        screenwidth (int): The width of the game screen.
        position (str): The position of the button on the screen.
        gap (int): The gap between buttons.
        y (int): The y-coordinate of the button.
        rect (pygame.Rect): The rectangle that represents the button.
        color (tuple): The color of the button.
        icon (pygame.Surface): The icon of the button.
        icon_rect (pygame.Rect): The rectangle that represents the icon.
    """

    def __init__(self, game, number, tooltip_text):
        """
        The constructor for the Button class.

        Parameters:
            game (object): The game object that this button is a part of.
            number (int): The number that identifies this button.
        """
        self.game = game
        self.number = number
        self.screenheight = self.game.height
        self.screenwidth = self.game.settings['WIDTH']
        self.position = self.game.settings['HOTBAR_POSITION']
        self.gap = self.game.settings['HEIGHT'] // 10

        self.y = self.screenheight // 10

        button_width = self.y - 20
        button_height = self.y - 20

        if self.number < 0:
            if self.position == 'bottom':
                x = self.screenwidth - self.gap * (-self.number - 1) - button_width - 10
                y = (self.screenheight - self.y) + (
                        (self.screenheight - (self.screenheight - self.y) - button_height) // 2)
            elif self.position == 'left':
                x = (self.screenwidth // 10 - button_width) // 2
                y = self.screenheight - self.gap * (-self.number - 1) - button_height - 10
            elif self.position == 'right':
                x = (self.screenwidth - self.screenwidth // 10) + (
                        (self.screenwidth - (self.screenwidth - self.screenwidth // 10) - button_width) // 2)
                y = self.screenheight - self.gap * (-self.number - 1) - button_height - 10
            elif self.position == 'top':
                x = self.screenwidth - self.gap * (-self.number - 1) - button_width - 10
                y = (self.y - button_height) // 2
        else:
            if self.position == 'bottom':
                x = self.gap * self.number + 10
                y = (self.screenheight - self.y) + (
                            (self.screenheight - (self.screenheight - self.y) - button_height) // 2)
            elif self.position == 'left':
                x = (self.screenwidth // 10 - button_width) // 2
                y = self.gap * self.number + 10
            elif self.position == 'right':
                x = (self.screenwidth - self.screenwidth // 10) + (
                            (self.screenwidth - (self.screenwidth - self.screenwidth // 10) - button_width) // 2)
                y = self.gap * self.number + 10
            elif self.position == 'top':
                x = self.gap * self.number + 10
                y = (self.y - button_height) // 2

        self.rect = pygame.Rect(x, y, button_width, button_height)

        if self.number == 0:
            self.color = (255, 0, 0)
            self.icon = images.torch_icon
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

        elif self.number == 1:
            self.color = (0, 0, 255)
            self.icon = images.object_icon
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

        elif self.number == 2:
            self.color = (0, 200, 0)
            self.icon = images.glass_icon
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

        elif self.number == 3:
            self.color = (0, 200, 100)
            self.icon = images.prism_icon
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

        elif self.number == 4:
            self.color = (5, 75, 60)
            self.icon = images.topopisy
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)
        elif self.number == 5:
            self.color = (64, 137, 189)
            self.icon = images.lens
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)
        elif self.number == 9:
            self.color = (155, 155, 155)
            self.icon = images.oneconvex
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)
        elif self.number == 7:
            self.color = (155, 155, 155)
            self.icon = images.concave
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)
        elif self.number == 8:
            self.color = (155, 155, 155)
            self.icon = images.oneconcave
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)
        elif self.number == 6:
            self.color = (253, 184, 38)
            self.icon = images.corridor_icon
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

        elif self.number == -1:
            self.color = None
            self.icon = images.exit_icon
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

        elif self.number == -2:
            self.color = None
            self.icon = images.settings_icon
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

        elif self.number == -3:
            self.color = None
            self.icon = images.puchar
            self.icon = pygame.transform.scale(self.icon, (button_width, button_height))
            self.icon_rect = self.icon.get_rect(center=self.rect.center)



        else:
            self.color = (20, 0, 0)

        self.tooltip_text = tooltip_text
        self.tooltip_font = pygame.font.Font(None, 24)

    def render(self):
        """
        Renders the button on the screen.
        """
        if self.color != None:
            pygame.draw.rect(self.game.screen, self.color, self.rect, 0, 5)

        try:
            self.game.screen.blit(self.icon, self.icon_rect)

        except:
            pass

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.show_tooltip()

    def show_tooltip(self):
        text_surface = self.tooltip_font.render(self.tooltip_text, True, (255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()

        text_rect = text_surface.get_rect()
        text_rect.bottomright = (mouse_pos[0]-5, mouse_pos[1]-5)

        pygame.draw.rect(self.game.screen, (0, 0, 0), text_rect.inflate(10, 10), 0, 5)

        self.game.screen.blit(text_surface, text_rect)

    def checkifclicked(self, mousepos):
        """
        Checks if the button was clicked and performs the corresponding action.

        Parameters:
            mousepos (tuple): The position of the mouse.
        """
        if self.rect.collidepoint(mousepos[0], mousepos[1]):
            if self.game.isDrawingModeOn != True:
                self.game.mixer.clicked_sound()
                if self.number == 0:
                    obj = gameobjects.Flashlight(self.game,
                                                 [(mousepos[0], mousepos[1]), (mousepos[0] + 200, mousepos[1]),
                                                  (mousepos[0] + 200, mousepos[1] + 100),
                                                  (mousepos[0], mousepos[1] + 100)], (255, 255, 255), 0.001, 0, 1,
                                                 image=images.torch)
                    self.game.current_flashlight = obj
                    self.game.achievements.handle_achievement_unlocked("let there be light")

                elif self.number == 1:
                    obj = gameobjects.Mirror(self.game, [(mousepos[0] - 100, mousepos[1] - 50),
                                                         (mousepos[0] + 100, mousepos[1] - 50),
                                                         (mousepos[0] + 100, mousepos[1] + 50),
                                                         (mousepos[0] - 100, mousepos[1] + 50)], (200, 200, 200), 0.001, 0, 0)
                    self.game.achievements.handle_achievement_unlocked("is it... me?")

                elif self.number == 2:
                    obj = gameobjects.ColoredGlass(self.game, [(mousepos[0] - 10, mousepos[1] - 50),
                                                               (mousepos[0] + 10, mousepos[1] - 50),
                                                               (mousepos[0] + 10, mousepos[1] + 50),
                                                               (mousepos[0] - 10, mousepos[1] + 50)], (0, 255, 0), 0, 1,
                                                   0)
                    self.game.achievements.handle_achievement_unlocked("some color in this black and white world")

                elif self.number == 3:
                    obj = gameobjects.Prism(self.game,
                                            [(mousepos[0] - 50, mousepos[1] + 20), (mousepos[0], mousepos[1] - 100*3**(1/2)/2),
                                             (mousepos[0] + 50, mousepos[1] + 20)], None, 0, 1, 0)
                    self.game.achievements.handle_achievement_unlocked("a whole new world")
                elif self.number == 5:
                    obj = gameobjects.Lens(self.game,
                                           [(mousepos[0] - 100, mousepos[1] - 100), (mousepos[0], mousepos[1] - 100),
                                            (mousepos[0], mousepos[1] + 100), (mousepos[0] - 100, mousepos[1] + 100)],
                                           (64, 137, 189), 0, 140, 1, 0, 140, refraction_index=1.5)
                    self.game.achievements.handle_achievement_unlocked("first step to... glasses")
                elif self.number == 9:
                    obj = gameobjects.Lens(self.game,
                                           [(mousepos[0] - 100, mousepos[1] - 100), (mousepos[0], mousepos[1] - 100),
                                            (mousepos[0], mousepos[1] + 100), (mousepos[0] - 100, mousepos[1] + 100)],
                                           (64, 137, 189), 0, 140, 1, 0, refraction_index=1.5)
                    self.game.achievements.handle_achievement_unlocked("first step to... glasses")
                elif self.number == 7:
                    obj = gameobjects.Lens(self.game,
                                           [(mousepos[0] - 100, mousepos[1] - 100), (mousepos[0], mousepos[1] - 100),
                                            (mousepos[0], mousepos[1] + 100), (mousepos[0] - 100, mousepos[1] + 100)],
                                           (64, 137, 189),  0, -140, 1, 0, -140, refraction_index=1.5)
                    self.game.achievements.handle_achievement_unlocked("first step to... glasses")
                elif self.number == 8:
                    obj = gameobjects.Lens(self.game,
                                           [(mousepos[0] - 100, mousepos[1] - 100), (mousepos[0], mousepos[1] - 100),
                                            (mousepos[0], mousepos[1] + 100), (mousepos[0] - 100, mousepos[1] + 100)],
                                           (64, 137, 189), 0, -140, 1, 0, refraction_index=1.5)
                    self.game.achievements.handle_achievement_unlocked("first step to... glasses")
                elif self.number == 6:
                    obj = gameobjects.Corridor(self.game, [(mousepos[0] - 100, mousepos[1] - 50),
                                                         (mousepos[0] + 100, mousepos[1] - 50),
                                                         (mousepos[0] + 100, mousepos[1] + 50),
                                                         (mousepos[0] - 100, mousepos[1] + 50)], None, 0, 0, 0, image_path=images.corridor)
                elif self.number == -1:
                    self.game.save_game()
                elif self.number == -2:
                    self.game.mode = 'settings'
                elif self.number == -3:
                    self.game.mode = 'achievements'
                try:
                    self.game.objects.append(obj)
                    obj.selected(mousepos)

                except:
                    pass
            if self.number == 4:
                if classes.game.isDrawingModeOn == True:
                    classes.game.isDrawingModeOn = False
                    classes.game.polygonDrawing.clearPoints(classes.game.polygonDrawing())

                elif classes.game.isDrawingModeOn == False:
                    classes.game.isDrawingModeOn = True
        if self.rect.collidepoint(mousepos[0], mousepos[1]) and not pygame.mouse.get_pressed()[0]:
            self.show_tooltip()




class ButtonForgame:
    """
    This class represents a Button for the game menu.

    Attributes:
        number (int): The number that identifies this button.
        screen (object): The screen object that this button is a part of.
        font (pygame.font.Font): The font used for the button text.
        width (int): The width of the button.
        height (int): The height of the button.
        y (int): The y-coordinate of the button.
        x (int): The x-coordinate of the button.
        rect (pygame.Rect): The rectangle that represents the button.
        text (pygame.Surface): The text of the button.
        textRect (pygame.Rect): The rectangle that represents the text.
    """
    def __init__(self, number, screen):
        """
        The constructor for the ButtonForgame class.

        Parameters:
            number (int): The number that identifies this button.
            screen (object): The screen object that this button is a part of.
        """
        self.number = number
        self.screen = screen
        self.screen.objects.append(self)
        self.font = pygame.font.Font(Font, self.screen.height // 35)

        self.width = self.screen.width // 3
        self.height = self.screen.height // 10

        # adjust y based on the number
        gap = 15
        self.y = (self.screen.height // 2) - self.height*1.2 + (self.height + gap) * number
        self.x = (self.screen.width // 12) - self.width // 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.number == 0:
            self.text = self.font.render('Start', True, 'black')

        elif self.number == 1:
            self.text = self.font.render('Settings', True, 'black')

        elif self.number == 3:
            self.text = self.font.render('Quit', True, 'black')

        elif self.number == 2:
            self.text = self.font.render('Achievements', True, 'black')

        elif self.number == 71:
            self.text = self.font.render('Back', True, 'black')
            self.y = self.screen.height - self.screen.height // 5
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        elif self.number == 72:
            self.text = self.font.render('New Save', True, 'black')
            if self.screen.state == 'presets':
                self.width = self.screen.width // 3
                self.y = (self.screen.height - self.screen.height // 10)
                self.x = (self.screen.width // 2) - self.width - gap
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            else:
                self.width = self.screen.width // 5
                self.y = (self.screen.height - self.screen.height // 10)
                self.x = (self.screen.width // 2) - self.width - self.width - gap
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        elif self.number == 73:
            self.text = self.font.render('Load Preset', True, 'black')
            self.width = self.screen.width // 5
            self.x = (self.screen.width // 2) - self.width
            self.y = (self.screen.height - self.screen.height // 10)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        elif self.number == 74:
            self.text = self.font.render('Back', True, 'black')
            if self.screen.state == 'presets':
                self.width = self.screen.width // 3
                self.y = (self.screen.height - self.screen.height // 10)
                self.x = (self.screen.width // 2) + gap
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            else:
                self.width = self.screen.width // 5
                self.y = (self.screen.height - self.screen.height // 10)
                self.x = (self.screen.width // 2) + self.width + gap*2
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


        elif self.number == 75:
            self.text = self.font.render('Delete', True, 'black')
            self.width = self.screen.width // 5
            self.y = (self.screen.height - self.screen.height // 10)
            self.x = (self.screen.width // 2) + gap
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        else:
            self.text = self.font.render('@', True, 'black')

        self.textRect = self.text.get_rect()
        self.textRect.center = (self.rect[0] + (self.rect[2] // 2), self.rect[1] + (self.rect[3] // 2))

    def checkcollision(self, pos):
        """
        Checks if the button was clicked and performs the corresponding action.

        Parameters:
            pos (tuple): The position of the mouse.
        """
        if self.rect.collidepoint(pos[0], pos[1]):
            if self.number == 0:
                self.screen.mode = 'loading'
                self.screen.mixer.clicked_sound()
            elif self.number == 1:
                self.screen.mode = 'settings'
                self.screen.mixer.clicked_sound()
            elif self.number == 3:
                self.screen.mixer.clicked_sound()
                exit()
            elif self.number == 2:
                self.screen.mode = 'achievements'
                self.screen.mixer.clicked_sound()
            elif self.number == 71:
                if type(self.screen) != music_settings.Music_settings_screen:
                    self.screen.game.mode = 'load_new_settings'
                    self.screen.mixer.clicked_sound()
                else:
                    self.screen.game.mode = 'settings'
                    self.screen.game.mixer.clicked_sound()
            elif self.number == 72:
                self.screen.game.mode = 'default'
                if self.screen.state == 'presets' and any(value for value in self.screen.game.selected_buttons.values()):
                    self.screen.game.preset = True
                self.screen.game.run = False
                self.screen.mixer.clicked_sound()
            elif self.number == 73:
                self.screen.state = 'presets'
                self.screen.mixer.clicked_sound()
            elif self.number == 74:
                if self.screen.state == 'default' and self.screen.action == 'default':
                    self.screen.game.mode = 'default'
                else:
                    self.screen.state = 'default'
                self.screen.mixer.clicked_sound()
            elif self.number == 75:
                self.screen.game.mode = 'delete'
                self.screen.mixer.clicked_sound()
            else:
                raise NotImplementedError('button function not yet added')

    def render(self):
        """
        Renders the button on the screen.
        """
        self.update()

        pygame.draw.rect(self.screen.screen, (255, 255, 255), self.rect, 0, 4)
        self.screen.screen.blit(self.text, self.textRect)

    def update(self):
        if self.number == 72:
            if any(value for value in self.screen.game.selected_buttons.values()):
                if self.screen.state == 'default':
                    self.text = self.font.render('Load Save', True, 'black')
                elif self.screen.state == 'presets':
                    self.text = self.font.render('Load Preset', True, 'black')
            else:
                self.text = self.font.render('New Save', True, 'black')
            self.textRect = self.text.get_rect()
            self.textRect.center = (self.rect[0] + (self.rect[2] // 2), self.rect[1] + (self.rect[3] // 2))

