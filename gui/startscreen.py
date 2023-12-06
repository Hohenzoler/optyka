import pygame

class Button:
    def __init__(self, StartScreen, rect):
        self.rect = rect
        self.startscreen = StartScreen
        self.startscreen.objects.append(self)

    def checkcollision(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            print('a')

    def render(self):
        pygame.draw.rect(self.startscreen.screen, (133,222,2), self.rect)



class StartScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.run = True
        self.objects = []

        b1 = Button(self, pygame.Rect(100, 100, 20, 20))

        self.mainloop()

    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.run = False

            for object in self.objects:
                object.render()
