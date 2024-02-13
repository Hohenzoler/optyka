import classes.game
import pygame

import settingsSetup
from classes import gameobjects, sounds, images, saveTK
from classes.font import Font


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

    def __init__(self, game, number):
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
            self.color = (0, 150, 0)
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
        elif self.number == 6:
            self.color = (64, 137, 189)
            self.icon = images.object_icon
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



        else:
            self.color = (20, 0, 0)

    def render(self):
        """
        Renders the button on the screen.
        """
        if self.color != None:
            pygame.draw.rect(self.game.screen, self.color, self.rect)

        try:
            self.game.screen.blit(self.icon, self.icon_rect)

        except:
            pass
    def checkifclicked(self, mousepos):
        """
        Checks if the button was clicked and performs the corresponding action.

        Parameters:
            mousepos (tuple): The position of the mouse.
        """
        if self.rect.collidepoint(mousepos[0], mousepos[1]):
            if self.number == 0:
                obj = gameobjects.Flashlight(self.game, [(mousepos[0], mousepos[1]), (mousepos[0] + 200, mousepos[1]), (mousepos[0] + 200, mousepos[1] + 100), (mousepos[0], mousepos[1] + 100)], (255, 255, 255), 0, 0.4, 0.5, image=images.torch)
                self.game.current_flashlight = obj
                self.game.achievements.handle_achievement_unlocked("first_flashlight_placed")

            elif self.number == 1:
                obj = gameobjects.Mirror(self.game, [(mousepos[0] - 100, mousepos[1] - 50), (mousepos[0] + 100, mousepos[1] - 50), (mousepos[0] + 100, mousepos[1] + 50), (mousepos[0] - 100, mousepos[1] + 50)], (255, 0, 0), 0, 0.9, 0.5, textureName='glass')
                self.game.achievements.handle_achievement_unlocked("first_mirror_placed")

            elif self.number == 2:
                obj = gameobjects.ColoredGlass(self.game, [(mousepos[0] - 10, mousepos[1] - 50), (mousepos[0] + 10, mousepos[1] - 50), (mousepos[0] + 10, mousepos[1] + 50), (mousepos[0] - 10, mousepos[1] + 50)], (0, 255, 0), 0, 0.4, 1)

            elif self.number == 3:
                obj = gameobjects.Prism(self.game, [(mousepos[0] - 50, mousepos[1]), (mousepos[0], mousepos[1] - 100), (mousepos[0] + 50, mousepos[1])], None, 0, 0.4, 0.5)

            elif self.number == 4:
                if classes.game.isDrawingModeOn == True:
                    classes.game.isDrawingModeOn = False

                elif classes.game.isDrawingModeOn == False:
                    classes.game.isDrawingModeOn = True
                    spiel = self.game
                # print(classes.game.isDrawingModeOn)
            elif self.number == 5:
                obj = gameobjects.Lens(self.game,
                                       [(mousepos[0] - 100, mousepos[1] - 100), (mousepos[0], mousepos[1] - 100),
                                        (mousepos[0], mousepos[1] + 100), (mousepos[0] - 100, mousepos[1] + 100)],
                                       (64, 137, 189), 0, 0 ,140, 0, 0.5)
            elif self.number == 6:
                obj = gameobjects.Lens(self.game,
                                       [(mousepos[0] - 100, mousepos[1] - 100), (mousepos[0], mousepos[1] - 100),
                                        (mousepos[0], mousepos[1] + 100), (mousepos[0] - 100, mousepos[1] + 100)],
                                       (64, 137, 189), 0, 2, 140, 0, 0.5)

            elif self.number == -1:
                self.game.generate_save()
                if len(self.game.objects) > 3:
                    if self.game.save_title != None:
                        prev_save_data = settingsSetup.load_settings(f'saves/{self.game.save_title}.json')
                        if len(prev_save_data) > 1:
                            if prev_save_data[1:] != self.game.save_obj[1:]:
                                pygame.mouse.set_visible(True)
                                a = saveTK.Save(self.game)
                        else:
                            pygame.mouse.set_visible(True)
                            a = saveTK.Save(self.game)
                    else:
                        pygame.mouse.set_visible(True)
                        a = saveTK.Save(self.game)

                elif len(self.game.objects) == 3 and self.game.save_title != None:
                    prev_save_data = settingsSetup.load_settings(f'saves/{self.game.save_title}.json')
                    if len(prev_save_data) != 1:
                        pygame.mouse.set_visible(True)
                        a = saveTK.Save(self.game)
                elif len(self.game.objects) == 3:
                    pass
                else:
                    pygame.mouse.set_visible(True)
                    a = saveTK.Save(self.game)
                self.game.run = False
            elif self.number == -2:
                self.game.mode = 'settings'


            try:
                self.game.objects.append(obj)
                obj.selected(mousepos)

            except:
                pass


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
        self.y = (self.screen.height // 2) - self.height // 2 + (self.height + gap) * number
        self.x = (self.screen.width // 12) - self.width // 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.number == 0:
            self.text = self.font.render('Start', True, 'black')

        elif self.number == 1:
            self.text = self.font.render('Settings', True, 'black')

        elif self.number == 2:
            self.text = self.font.render('Quit', True, 'black')

        elif self.number == 71:
            self.text = self.font.render('Back', True, 'black')
            self.y = self.screen.height - self.screen.height // 5
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        elif self.number == 72:
            self.text = self.font.render('New Game', True, 'black')
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
            self.width = self.screen.width // 5
            self.y = (self.screen.height - self.screen.height // 10)
            self.x = (self.screen.width // 2) + self.width + gap*2
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        elif self.number == 75:
            self.text = self.font.render('Delete', True, 'black')
            self.width = self.screen.width // 5
            self.y = (self.screen.height - self.screen.height // 10)
            self.x = (self.screen.width // 2) + gap
            print(self.x)
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
                sounds.clicked_sound()
            elif self.number == 1:
                self.screen.mode = 'settings'
                sounds.clicked_sound()
            elif self.number == 2:
                sounds.clicked_sound()
                exit()
            elif self.number == 71:
                self.screen.game.mode = 'load_new_settings'
                sounds.clicked_sound()
            elif self.number == 72:
                self.screen.game.mode = 'default'
                self.screen.game.run = False
                sounds.clicked_sound()
            elif self.number == 74:
                self.screen.game.mode = 'default'
                sounds.clicked_sound()
            elif self.number == 75:
                self.screen.game.mode = 'delete'
                sounds.clicked_sound()
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
            if any(value for value in self.screen.game.selected_buttons.values()) == True:
                self.text = self.font.render('Load Game', True, 'black')
            else:
                self.text = self.font.render('New Game', True, 'black')
            self.textRect = self.text.get_rect()
            self.textRect.center = (self.rect[0] + (self.rect[2] // 2), self.rect[1] + (self.rect[3] // 2))

