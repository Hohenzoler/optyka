import pygame
import os


class Save:
    def __init__(self, game):
        self.game = game
        self.input_box = pygame.Rect(100, 100, 140, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.save_button = pygame.Rect(100, 150, 100, 32)
        self.dont_save_button = pygame.Rect(210, 150, 100, 32)
        self.cancel_button = pygame.Rect(320, 150, 100, 32)

    def render(self):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.game.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.game.screen, self.color, self.input_box, 2)

        pygame.draw.rect(self.game.screen, (0, 255, 0), self.save_button)
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.dont_save_button)
        pygame.draw.rect(self.game.screen, (255, 255, 0), self.cancel_button)

        save_text = self.font.render('Save', True, (0, 0, 0))
        dont_save_text = self.font.render("Don't Save", True, (0, 0, 0))
        cancel_text = self.font.render('Cancel', True, (0, 0, 0))

        self.game.screen.blit(save_text, (self.save_button.x + 10, self.save_button.y + 5))
        self.game.screen.blit(dont_save_text, (self.dont_save_button.x + 10, self.dont_save_button.y + 5))
        self.game.screen.blit(cancel_text, (self.cancel_button.x + 10, self.cancel_button.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

            if self.save_button.collidepoint(event.pos):
                self.save()
            elif self.dont_save_button.collidepoint(event.pos):
                self.dont_save()
            elif self.cancel_button.collidepoint(event.pos):
                self.cancel()

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.save()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def save(self):
        save_title = self.text.strip()
        if save_title != '':
            save_title = save_title.replace(' ', "_")
            self.old_save_title = self.game.save_title
            self.game.save_title = save_title

            self.dir = "saves"
            self.saves_files = [file[:-5] for file in os.listdir(self.dir) if file.endswith('.json')]

            if self.game.save_title in self.saves_files and self.game.save_title != self.old_save_title:
                print("Error: You cannot save your game with the same name as another save file.")
            else:
                self.game.save_to_file()
                self.game.response_received = True  # Set response received flag

    def dont_save(self):
        self.game.response_received = True  # Set response received flag

    def cancel(self):
        self.game.cancel = True
        self.game.response_received = True  # Set response received flag