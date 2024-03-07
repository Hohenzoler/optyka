import pygame
from classes import gameobjects

class Camera:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:  # Right arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0] - 10, self.game.points[i][1])

            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x - 10, obj.rect.y, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0] - 10, obj.points[i][1])

        if keys[pygame.K_LEFT]:  # Left arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0] + 10, self.game.points[i][1])

            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x + 10, obj.rect.y, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0] + 10, obj.points[i][1])

        if keys[pygame.K_UP]:  # Up arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0], self.game.points[i][1] + 10)
            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x, obj.rect.y + 10, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0], obj.points[i][1] + 10)

        if keys[pygame.K_DOWN]:  # Down arrow key is held down
            for i in range(len(self.game.points)):
                self.game.points[i] = (self.game.points[i][0], self.game.points[i][1] - 10)

            for obj in self.game.objects:
                if isinstance(obj, gameobjects.GameObject):
                    obj.rect = pygame.Rect(obj.rect.x, obj.rect.y - 10, obj.rect.width, obj.rect.height)
                    for i in range(len(obj.points)):
                        obj.points[i] = (obj.points[i][0], obj.points[i][1] - 10)
