import pygame
from gui import button


pygame.init()

class StartScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.run = True
        self.objects = []
        self.font = pygame.font.Font('freesansbold.ttf', self.width//20)
        self.maintext = self.font.render('Optyka', True, 'white')
        self.maintextRect = self.maintext.get_rect()
        self.maintextRect.center = (width//2, (height//2) - 200)


        pygame.display.set_caption('Optyka')

        self.buttons = [button.ButtonForStartScreen(x, self) for x in range(3)]

        self.mainloop()

    def mainloop(self):
        while self.run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.run = False


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for object in self.objects:
                        if type(object) == button.ButtonForStartScreen:
                            object.checkcollision(event.pos)


            for object in self.objects:
                object.render()

            self.screen.blit(self.maintext, self.maintextRect)

            pygame.display.update()
