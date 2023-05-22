

import pygame
import sys


class Player:
    def __init__(self, name):
        self.name = name
        self.active = False
        self.kick_confirmation = False


class ServerUser:
    def __init__(self, main):
        self.background_image = pygame.image.load("Material/BG/Title.png")
        self.screen = main.screen
        self.screen_width = main.screen.get_width()
        self.screen_height = main.screen.get_height()
        self.popup_width = self.screen_width//6
        self.popup_height = self.screen_height // 12
        self.font = pygame.font.Font(None, int(self.screen_width / 30))
        self.button_size = (50, 30)  # Reduced button height
        self.ORANGE = (255, 163, 0)
        self.button_color = self.ORANGE
        self.offset = self.screen_width//10
        self.players = [Player(f"player{i}") for i in range(6)]
        self.player_rects = []
        self.button_rects = []
        self.box_width = self.screen_width // 3
        self.box_height = (self.screen_height) // 6

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, player_rect in enumerate(self.player_rects):
                        if player_rect.collidepoint(event.pos):
                            self.players[i].active = not self.players[i].active
                            self.players[i].kick_confirmation = False

                    for i, button_rect in enumerate(self.button_rects):
                        if button_rect.collidepoint(event.pos) and self.players[i].active:
                            self.players[i].kick_confirmation = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    for player in self.players:
                        player.kick_confirmation = False

            self.screen.blit(self.background_image, (0, 0))
            self.draw_player_boxes()
            self.draw_kick_buttons()
            self.draw_kick_confirmation()
            pygame.display.flip()

    def draw_player_boxes(self):
        for i, player in enumerate(self.players):
            if not player.kick_confirmation:
                color = (0, 255, 0) if player.active else (150, 150, 150)
                box_x = self.screen_width // 3
                box_y = 50 + (self.box_height + 20) * i
                rect = pygame.Rect(
                    box_x, box_y, self.box_width, self.box_height)
                pygame.draw.rect(self.screen, color, rect)
                self.player_rects.append(rect)

                text = self.font.render(player.name, True, (255, 255, 255))
                text_rect = text.get_rect(
                    top=box_y + self.offset, left=box_x + self.offset)
                self.screen.blit(text, text_rect)

    def draw_kick_buttons(self):
        self.button_rects = []
        for i, player in enumerate(self.players):
            if player.active and not player.kick_confirmation:
                box_x = self.screen_width // 3
                box_y = 50 + (self.box_height + 20) * i
                button_x = box_x + self.box_width + self.offset
                button_y = box_y + (self.box_height - self.button_height) // 2
                button_rect = pygame.Rect(
                    button_x, button_y, self.button_width, self.button_height)
                pygame.draw.rect(self.screen, self.button_color, button_rect)
                self.button_rects.append(button_rect)

                text = self.font.render("Kick", True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(button_x + self.button_width // 2, button_y + self.button_height // 2))
                self.screen.blit(text, text_rect)

    def draw_kick_confirmation(self):
        for player in self.players:
            if player.kick_confirmation:

                popup_x = (self.screen_width - self.popup_width) // 2
                popup_y = (self.screen_height - self.popup_height) // 2
                popup_rect = pygame.Rect(
                    popup_x, popup_y, self.popup_width, self.popup_height)
                pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)

                font = self.font
                text = font.render(f"Kick {player.name}?", True, (0, 0, 0))
                text_rect = text.get_rect(center=popup_rect.center)
                self.screen.blit(text, text_rect)

                button_x = popup_x + self.popup_width // 4
                button_y = popup_y + self.popup_height // 2
                button_spacing = 20
                yes_button_rect = pygame.Rect(
                    button_x, button_y, self.button_size[0], self.button_size[1])
                no_button_rect = pygame.Rect(
                    button_x + self.popup_width // 2 + button_spacing, button_y, self.button_size[0], self.button_size[1])
                pygame.draw.rect(self.screen, (0, 255, 0), yes_button_rect)
                pygame.draw.rect(self.screen, (255, 0, 0), no_button_rect)

                yes_text = font.render("Y", True, (255, 255, 255))
                no_text = font.render("N", True, (255, 255, 255))
                self.screen.blit(yes_text, yes_button_rect)
                self.screen.blit(no_text, no_button_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if yes_button_rect.collidepoint(event.pos):
                            player.active = False
                            player.kick_confirmation = False

                        if no_button_rect.collidepoint(event.pos):
                            player.kick_confirmation = False
