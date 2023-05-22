import pygame
import sys

import pygame
import sys
class Player:
    def __init__(self, name):
        self.name = name
        self.activeBox = False
        self.online = False
        self.kick_confirmation = False

class PasswordBox:
    def __init__(self, screen, x, y, width, height, font):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.password = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.password = self.password[:-1]
            else:
                self.password += event.unicode

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)
        text_surface = self.font.render(self.password, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

class ClientUser:
    def __init__(self,main):
        self.background_image = pygame.image.load("Material/BG/Title.png")
        self.screen = main.screen
        self.screen_width = main.screen.get_width()
        self.screen_height = main.screen.get_height()
        self.popup_width = 30
        self.popup_height = 10
        self.font = pygame.font.Font(None, int(self.screen_width / 30))
        self.players = [Player(f"Player {i + 1}") for i in range(6)]
        self.player_rects = []
        self.button_size = (50, 30)  # Reduced button height
        self.ORANGE = (255, 163, 0)
        self.button_color = self.ORANGE
        self.offset = 5
        self.current_players = []  # List to store current players
        self.player_rects = []
        self.box_width = 100
        self.box_height = 50


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.mouse_pos = pygame.mouse.get_pos()  
                # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                #     for i, player_rect in enumerate(self.player_rects):
                #         if player_rect.collidepoint(self.mouse_pos):
                #             player = self.players[i]
                #             player.activeBox = not player.activeBox
                #             player.kick_confirmation = False
                #             player.online=True
                        
                        
            self.screen.blit(self.background_image, (0, 0))
            self.draw_player_boxes()
            pygame.display.flip()

    def draw_player_boxes(self):
            self.player_rects = []
            for i, player in enumerate(self.players):
                color = (0, 255, 0) if player.activeBox else (150, 150, 150)
                box_x = 200
                box_y = 50 + (self.box_height + 20) * i
                rect = pygame.Rect(
                    box_x, box_y, self.box_width, self.box_height)
                pygame.draw.rect(self.screen, color, rect)
                self.player_rects.append(rect)

                text = self.font.render(player.name, True, (255, 255, 255))
                text_rect = text.get_rect(
                    top=box_y + self.offset, left=box_x + self.offset)
                self.screen.blit(text, text_rect)