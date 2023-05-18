import pygame
import sys


class ClientUser:
    def __init__(self):
        self.current_players = []  # List to store current players
        self.screen = None  # Pygame screen object
        self.font = None  # Pygame font object

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.Font(None, 24)

    def show_input_window(self, prompt):
        input_text = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return input_text
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            self.screen.fill((255, 255, 255))
            prompt_text = self.font.render(prompt, True, (0, 0, 0))
            input_text_surface = self.font.render(input_text, True, (0, 0, 0))
            self.screen.blit(prompt_text, (100, 100))
            self.screen.blit(input_text_surface, (100, 140))
            pygame.display.update()

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


# Example usage
client = ClientUser()
client.run()
