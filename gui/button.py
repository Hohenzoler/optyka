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
        mousepos[0] -= 100  # Centering the mouse
        mousepos[1] -= 50

        self.f = gameobjects.Flashlight(self.game, [(mousepos[0], mousepos[1]),
                                        (mousepos[0] + 200, mousepos[1]),
                                        (mousepos[0] + 200, mousepos[1] + 100),
                                        (mousepos[0], mousepos[1] + 100)], (255, 0, 0), 100, image_path="images/torch.png")
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
                    adjust_flashlight()
                else:
                    adjust_flashlight()
                self.f.drawoutline()



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
                            (mousepos[0], mousepos[1]),
                            (mousepos[0] + 200, mousepos[1]),
                            (mousepos[0] + 200, mousepos[1] + 100),
                            (mousepos[0], mousepos[1] + 100)
                        ],
                        (255, 0, 0),
                        100,
                        image_path="images/torch.png"
                    )
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



