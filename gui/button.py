import pygame
from classes import gameobjects, sounds
from classes import images

class Button:
    def __init__(self, game, number):
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
        elif self.number == 1:
            self.color = (0, 0, 255)
        elif self.number == 2:
            self.color = (0, 255, 0)
        elif self.number == 3:
            self.color = (0, 200, 100)
        elif self.number == 4:
            self.color = (5, 75, 60)
        else:
            self.color = (20, 0, 0)

        self.clicked = 0  # 0 means the button is not clicked, 1 means the button was clicked and is currently active and 2 means that the selectd object is being placed and the button will revert to 0 afterwards.

        self.torch_icon = images.torch_icon
        # Scale the torch icon to the size of the button
        self.torch_icon = pygame.transform.scale(self.torch_icon, (button_width, button_height))
        self.object_icon = images.object_icon

        self.prism_icon = images.prism_icon
        self.prism_icon = pygame.transform.scale(self.prism_icon, (button_width, button_height))

        # Scale the object icon to the size of the button
        self.object_icon = pygame.transform.scale(self.object_icon, (button_width, button_height))

        self.settings_icon = images.settings_icon
        self.settings_icon = pygame.transform.scale(self.settings_icon, (button_width, button_height))
        self.settings_icon_rect = self.settings_icon.get_rect(center=self.rect.center)

        self.exit_icon = images.exit_icon
        self.exit_icon = pygame.transform.scale(self.exit_icon, (button_width, button_height))
        self.exit_icon_rect = self.exit_icon.get_rect(center=self.rect.center)

        self.topopisy_icon = images.topopisy
        self.topopisy_icon = pygame.transform.scale(self.topopisy_icon, (button_width, button_height))
        self.topopisy_icon_rect = self.topopisy_icon.get_rect(center=self.rect.center)

        self.shape_of_mirror = None

    def render(self):
        # Render GUI elements
        mousepos = list(pygame.mouse.get_pos())
        # mousepos[0] -= 100  # Centering the mouse
        # mousepos[1] -= 50

        # self.f = gameobjects.Flashlight(self.game, [(mousepos[0], mousepos[1]),
        #                                 (mousepos[0] + 200, mousepos[1]),
        #                                 (mousepos[0] + 200, mousepos[1] + 100),
        #                                 (mousepos[0], mousepos[1] + 100)], (255, 0, 0), self.game.current_angle, image_path="images/torch.png")
        self.f = self.game.current_flashlight

        def adjust_flashlight():
            self.f.adjust(mousepos[0], mousepos[1], 0)

        if self.number != -2 and self.number != -1:
            pygame.draw.rect(self.game.screen, self.color, self.rect)
        if self.number == 0:
            torch_icon_rect = self.torch_icon.get_rect(center=self.rect.center)
            self.game.screen.blit(self.torch_icon, torch_icon_rect)
            if self.clicked == 1:
                if self.game.r:
                    self.f.adjust(mousepos[0], mousepos[1], self.game.r)
                    self.game.r = False
                else:
                    adjust_flashlight()

                self.f.drawoutline()
                # print(self.f.angle)

            if self.clicked == 2:
                adjust_flashlight()

                self.f.light_adjust(self.f.points[0][0], self.f.points[0][1])
                print(self.f.points[0][0], self.f.points[0][1])
                self.game.objects.insert(-2, self.f)
                self.clicked = 0
                self.f = None
                sounds.laser_sound()



        elif self.number == 1:
            object_icon_rect = self.object_icon.get_rect(center=self.rect.center)
            self.game.screen.blit(self.object_icon, object_icon_rect)
            if self.clicked == 1:
                self.m.adjust(mousepos[0], mousepos[1], 0)

            if self.clicked == 2:
                print(self.m.points)
                print(mousepos)
                self.game.objects.insert(-2, self.m)
                self.clicked = 0

        # future prism
        elif self.number == 3:
            self.prism_icon_rect = self.prism_icon.get_rect(center=self.rect.center)
            self.game.screen.blit(self.prism_icon, self.prism_icon_rect)
            if self.clicked == 1:
                self.p.adjust(mousepos[0], mousepos[1], 0)

            if self.clicked == 2:
                print(self.p.points)
                print(mousepos)
                self.game.objects.insert(-2, self.p)
                self.clicked = 0

        elif self.number == 4:
            self.game.screen.blit(self.topopisy_icon, self.topopisy_icon_rect)

        if self.number == -2:
            self.game.screen.blit(self.settings_icon, self.settings_icon_rect)

        if self.number == -1:
            self.game.screen.blit(self.exit_icon, self.exit_icon_rect)

    def checkifclicked(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            mousepos = pygame.mouse.get_pos()
            if self.clicked == 0:
                self.clicked = 1
                if self.number == 0:
                    self.f = gameobjects.Flashlight(
                        self.game,
                        [
                            (mousepos[0] - 100, mousepos[1] - 50),
                            (mousepos[0] - 100, mousepos[1] + 50),
                            (mousepos[0] + 100, mousepos[1] + 50),
                            (mousepos[0] + 100, mousepos[1] - 50)
                        ],
                        (255, 0, 0),
                        0,
                        image=images.torch
                    )
                    self.game.current_flashlight = self.f
                    # self.f.selected(mousepos)
                    sounds.selected_sound()
                elif self.number == 1:
                    self.m = gameobjects.Mirror(self.game, [(mousepos[0] - 100, mousepos[1] - 50),
                                                            (mousepos[0] + 100, mousepos[1] - 50),
                                                            (mousepos[0] + 100, mousepos[1] + 50),
                                                            (mousepos[0] - 100, mousepos[1] + 50)], (255, 0, 0), 0)
                    sounds.selected_sound()

                elif self.number == 2:
                    sounds.selected_sound()

                elif self.number == 3:
                    self.p = gameobjects.Prism(self.game,
                                               [
                                                   (mousepos[0] + 150, mousepos[1]),
                                                   (mousepos[0] + 100, mousepos[1] - 100),
                                                   (mousepos[0] + 50, mousepos[1])],
                                               (255, 0, 0), 100)
                    sounds.selected_sound()

                elif self.number == 4:
                    sounds.selected_sound()

                elif self.number == -1:
                    self.game.run = False

                elif self.number == -2:
                    self.game.mode = 'settings'
                    sounds.clicked_sound()






            elif self.rect.collidepoint(mousepos) and self.clicked == 1:
                self.clicked = 0
                sounds.selected_sound()
        elif self.rect.collidepoint(pos) is False and self.clicked == 1:

            self.clicked = 2


class ButtonForgame:
    def __init__(self, number, screen):
        self.number = number
        self.screen = screen
        self.screen.objects.append(self)
        self.font = pygame.font.Font('freesansbold.ttf', self.screen.height // 35)

        self.width = self.screen.width // 3
        self.height = self.screen.height // 10

        # adjust y based on the number
        gap = 15
        self.y = (self.screen.height // 2) - self.height // 2 + (self.height + gap) * number
        self.x = (self.screen.width // 2) - self.width // 2
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

        else:
            self.text = self.font.render('@', True, 'black')

        self.textRect = self.text.get_rect()
        self.textRect.center = (self.rect[0] + (self.rect[2] // 2), self.rect[1] + (self.rect[3] // 2))

    def checkcollision(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            if self.number == 0:
                self.screen.run = False
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
            else:
                raise NotImplementedError('button function not yet added')

    def render(self):
        pygame.draw.rect(self.screen.screen, (255, 255, 255), self.rect, 0, 4)
        self.screen.screen.blit(self.text, self.textRect)
