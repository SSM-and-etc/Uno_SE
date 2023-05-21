import pygame
import sys


class ClientUser:
    def __init__(self):
        self.current_players = []  # List to store current players
        self.screen = None  # Pygame screen object
        self.font = None  # Pygame font object

    def show_lobby(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))
            players_text = self.font.render(
                "Current Players:", True, (0, 0, 0))
            self.screen.blit(players_text, (100, 100))
            y_position = 140
            for player in self.current_players:
                player_text = self.font.render(player, True, (0, 0, 0))
                self.screen.blit(player_text, (100, y_position))
                y_position += 30
            pygame.display.update()

    def run(self):
        self.initialize()
        server_address = self.show_input_window("Enter server address:")
        server_password = self.show_input_window("Enter server password:")
        # Connect to the server using the provided address and password

        # Retrieve and update the list of current players from the server using the lobby object
        self.current_players = ["Player1", "Player2", "Player3"]

        self.show_lobby()

