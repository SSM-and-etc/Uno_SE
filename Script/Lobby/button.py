import pygame
class StartButton:
    def __init__(self, msg, x, y, w, h, color,font, screen, action):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.font = font
        self.screen = screen
        self.action = action  # Button action
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        text_surf, text_rect = self.text_objects(self.msg, self.font)
        text_rect.center = self.rect.center
        self.screen.blit(text_surf, text_rect)
        

    def handle_event(self,event):   
      if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

    def text_objects(self, text, font):
        text_surface = font.render(text, True, pygame.Color('black'))
        return text_surface, text_surface.get_rect()

