import pygame

pygame.init()
class Button:
    def __init__(self, number, StartScreen):
        self.number = number
        self.startscreen = StartScreen
        self.startscreen.objects.append(self)
        self.font = pygame.font.Font('freesansbold.ttf',  20)


        if self.number == 0:
            self.width = self.startscreen.width//3
            self.height = self.startscreen.height//10

            self.x = (self.startscreen.width//2) - self.width//2
            self.y = (self.startscreen.height // 2) - self.height // 2

            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


            self.text = self.font.render('Start', True, 'black')
            self.textRect = self.text.get_rect()
            self.textRect.center = (self.rect[0] + (self.rect[2] // 2), self.rect[1] + (self.rect[3] // 2))

    def checkcollision(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.startscreen.run = False

    def render(self):
        pygame.draw.rect(self.startscreen.screen, (255,255,255), self.rect)
        # Main game loop

        self.startscreen.screen.blit(self.text, self.textRect)


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

        playbutton = Button(0, self)

        self.mainloop()

    def mainloop(self):
        while self.run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for object in self.objects:
                        if type(object) == Button:
                            object.checkcollision(event.pos)


            for object in self.objects:
                object.render()

            self.screen.blit(self.maintext, self.maintextRect)

            pygame.display.update()
