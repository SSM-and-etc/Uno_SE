import pygame
import sys

class Player:
    def __init__(self, name):
        self.name = name
        self.activeBox = False
        self.online = False
        self.kick_confirmation = False

class ServerUser:
    def __init__(self, main):
        self.background_image = pygame.image.load("Material/BG/Title.png")
        self.screen = main.screen
        self.screen_width = main.screen.get_width()
        self.screen_height = main.screen.get_height()
        self.popup_width = 30
        self.popup_height = 10
        self.font = pygame.font.Font(None, int(self.screen_width / 30))
        self.button_size = (50, 30)  # Reduced button height
        self.ORANGE = (255, 163, 0)
        self.button_color = self.ORANGE
        self.offset = 5
        self.players = [Player(f"Player {i + 1}") for i in range(6)]
        self.player_rects = []
        self.button_rects = []
        self.box_width = 150
        self.box_height = 50
        self.box_x= 0
        self.box_y=0
        self.ip_box = pygame.Rect(self.screen_width - 250, 50, 200, 30)
        self.password_box = pygame.Rect(self.screen_width - 250, 90, 200, 30)
        self.start_button = pygame.Rect(
        self.screen_width - 150, self.screen_height - 80, 100, 50)
        self.mouse_pos=None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.mouse_pos = pygame.mouse.get_pos()  
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    for i, player_rect in enumerate(self.player_rects):
                        if player_rect.collidepoint(self.mouse_pos):
                            player = self.players[i]
                            player.activeBox = not player.activeBox
                            player.kick_confirmation = False
                            player.online=True
                            
                    if self.start_button.collidepoint(self.mouse_pos):
                        self.start_game()

                for i, button_rect in enumerate(self.button_rects):
                        if button_rect.collidepoint(self.mouse_pos):
                            player.kick_confirmation = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    for player in self.players:
                        player.kick_confirmation = False
                        
            self.screen.blit(self.background_image, (0, 0))
            self.draw_player_boxes()
            self.draw_kick_buttons()
            self.draw_kick_confirmation()
            self.draw_ip_password_boxes() 
            self.draw_start_button()  
            pygame.display.flip()


    def start_game(self):
        print("Game started!")
        
    def update_player_names(self):
        for player in self.players:
            if player.activeBox:
                player.name = self.players[self.players.index(player)].name
            else:
                player.name = ""

    def draw_player_boxes(self):
        self.player_rects = []
        for i, player in enumerate(self.players):
            color = (0, 255, 0) if player.activeBox else (150, 150, 150)
            self.box_x = 200
            self.box_y = 50 + (self.box_height + 20) * i
            rect = pygame.Rect(
                self.box_x, self.box_y, self.box_width, self.box_height)
            pygame.draw.rect(self.screen, color, rect)
            self.player_rects.append(rect)

            text = self.font.render(player.name, True, (255, 255, 255))
            text_rect = text.get_rect(
                top=self.box_y + self.offset, left=self.box_x + self.offset, width=self.box_width - self.offset * 2)
            self.screen.blit(text, text_rect)

    def draw_kick_buttons(self):

        for i, player in enumerate(self.players):
            if player.activeBox:
                self.box_x = 200
                self.box_y = 50 + (self.box_height + 20) * i
                button_x = self.box_x + self.box_width + self.offset
                button_y = self.box_y + (self.box_height - self.button_size[1]) // 2
                button_rect = pygame.Rect(
                    button_x, button_y, self.button_size[0], self.button_size[1])
                pygame.draw.rect(self.screen, self.button_color, button_rect)
                self.button_rects.append(button_rect)

                text = self.font.render("Kick", True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(button_x + self.button_size[0] // 2, button_y + self.button_size[1] // 2))
                self.screen.blit(text, text_rect)

    def draw_kick_confirmation(self):
        for player in self.players:
            if player.activeBox:
                if player.kick_confirmation:
                    player_index = self.players.index(player)
                    print(player_index)
                    button_rect = self.button_rects[player_index]
                    button_x = button_rect.x + button_rect.width
                    button_y = button_rect.y
                    button_spacing = 20
                    popup_x = button_x + button_rect.width + self.offset
                    popup_y = button_y+(button_rect.height - self.popup_height) // 2
                    popup_rect = pygame.Rect(
                        popup_x, popup_y, self.popup_width, self.popup_height)
                    pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)

                    font = self.font
                    text = font.render(f"Kick {player.name}?", True, (0, 0, 0))
                    text_rect = text.get_rect(center=popup_rect.center)
                    self.screen.blit(text, text_rect)

                    yes_button_rect = pygame.Rect(
                        popup_x + self.popup_width // 4, popup_y, self.button_size[0], self.button_size[1])
                    no_button_rect = pygame.Rect(
                        popup_x + self.popup_width // 2 + button_spacing, popup_y, self.button_size[0], self.button_size[1])
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
                            if yes_button_rect.collidepoint(self.mouse_pos):
                                player.activeBox = False
                                player.kick_confirmation = False

                            if no_button_rect.collidepoint(self.mouse_pos):
                                player.kick_confirmation = False
                                
    def draw_ip_password_boxes(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.ip_box, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), self.password_box, 2)

    def draw_start_button(self):
        pygame.draw.rect(self.screen, self.button_color, self.start_button)
        text = self.font.render("Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.start_button.center)
        self.screen.blit(text, text_rect)

