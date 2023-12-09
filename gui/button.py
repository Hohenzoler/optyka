import pygame
from classes import gameobjects, sounds

class Button:
    def __init__(self, game, number, width, y, position):
        self.game = game
        self.number = number
        self.screenheight = self.game.height
        self.y = y
        self.guiwith = width

        self.position = position

        if self.position == 'buttom':
            self.rect = pygame.Rect(60 * self.number + 10, self.screenheight - self.y + 10, self.y - 20, self.y - 20)
        elif self.position == 'left':
            self.rect = pygame.Rect(20, 60 * self.number + 10, self.y - 10, self.y - 20)
        elif self.position == 'right':
            self.rect = pygame.Rect(self.guiwith - self.y, 60 * self.number + 10, self.y - 20, self.y - 20)
        elif self.position == 'top':
            self.rect = pygame.Rect(60 * self.number + 10, 10, self.y - 20, self.y - 20)


        if self.number == 0:
            self.color = (255, 0, 0)
        elif self.number == 1:
            self.color = (0, 0, 255)
        elif self.number == 2:
            self.color = (0, 255, 0)
        else:
            self.color = (255, 255, 255)

        self.clicked = 0 #0 means the button is not clicked, 1 means the button was clicked and is currently active and 2 means that the selectd object is being placed and the button will revert to 0 afterwards.

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
        self.m = gameobjects.Mirror(self.game, [(mousepos[0], mousepos[1]),
                                                (mousepos[0] + 200, mousepos[1]),
                                                (mousepos[0] + 50, mousepos[1] + 100),
                                                (mousepos[0] -20, mousepos[1]-100),
                                                (mousepos[0], mousepos[1] + 100)], (255, 0, 0), 100)


        def adjust_flashlight():
            self.f.adjust(mousepos[0], mousepos[1], 0)

        if self.number == 0:
            if self.clicked == 1:
                if self.game.r:
                    #self.f.angle+=1
                    self.f.adjust(mousepos[0], mousepos[1], 1)
                    adjust_flashlight()
                else:
                    adjust_flashlight()

                self.f.drawoutline()
                print(self.f.angle)



            if self.clicked == 2:
                if self.game.r:
                    adjust_flashlight()
                else:
                    adjust_flashlight()

                self.f.light_adjust(self.f.points[0][0], self.f.points[0][1])
                self.game.objects.insert(-2, self.f)
                self.clicked = 0
                self.f = None
                sounds.placed_sound()



        elif self.number == 1:
            if self.clicked == 1:
                self.m.adjust(mousepos[0], mousepos[1], 0)
            if self.clicked == 2:
                self.game.objects.insert(-2, self.m)
                self.clicked = 0


        pygame.draw.rect(self.game.screen, self.color, self.rect)

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
                        image_path="images/torch.png"
                    )
                    self.game.current_flashlight = self.f
                    # self.f.selected(mousepos)
                elif self.number == 1:
                    self.m = gameobjects.Mirror(self.game, [(mousepos[0], mousepos[1]),
                                                    (mousepos[0] + 200, mousepos[1]),
                                                    (mousepos[0] + 50, mousepos[1] + 100),
                                                    (mousepos[0] -20, mousepos[1]-100),
                                                    (mousepos[0], mousepos[1] + 100)], (255, 0, 0), 100)




                sounds.selected_sound()

            elif self.rect.collidepoint(mousepos) and self.clicked == 1:
                self.clicked = 0
                sounds.selected_sound()
        elif self.rect.collidepoint(pos) is False and self.clicked == 1:
            self.clicked = 2



class ButtonForStartScreen:
    def __init__(self, number, StartScreen):
        self.number = number
        self.startscreen = StartScreen
        self.startscreen.objects.append(self)
        self.font = pygame.font.Font('freesansbold.ttf',  self.startscreen.height//35)

        self.width = self.startscreen.width // 3
        self.height = self.startscreen.height // 10


        #adjust y based on the number
        gap = 15
        self.y = (self.startscreen.height // 2) - self.height // 2 + (self.height + gap) * number
        self.x = (self.startscreen.width // 2) - self.width // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.number == 0:
            self.text = self.font.render('Start', True, 'black')

        elif self.number == 1:
            self.text = self.font.render('Settings', True, 'black')

        elif self.number == 71:
            self.text = self.font.render('Save and Exit', True, 'black')
            self.y = self.startscreen.height - self.startscreen.height//5
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        else:
            self.text = self.font.render('@', True, 'black')

        self.textRect = self.text.get_rect()
        self.textRect.center = (self.rect[0] + (self.rect[2] // 2), self.rect[1] + (self.rect[3] // 2))

    def checkcollision(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            if self.number == 0:
                self.startscreen.run = False
            elif self.number == 1:
                self.startscreen.mode = 'settings'
            elif self.number == 71:
                self.startscreen.mode = 'load_new_settings'
            else:
                raise NotImplementedError('button function not yet added')


    def render(self):
        pygame.draw.rect(self.startscreen.screen, (255,255,255), self.rect)
        self.startscreen.screen.blit(self.text, self.textRect)

