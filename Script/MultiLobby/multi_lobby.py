import pygame

from ServerUser.server_user import ServerUser
from ClientUser.client_user import ClientUser


class MultiLobby:
    def __init__(self,main):
        # Initialize Pygame
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        # Define button properties
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_SPACING = 20
        self.BUTTON_COLOR = (0, 255, 0)
        self.TEXT_COLOR = (255, 255, 255)
        self.FONT_SIZE = 24

        # Create Server and Client objects
        self.server = None
        self.client = None

    def handle_button_click(self, button_name):
        if button_name == "방만들기":
            self.server = ServerUser()
        elif button_name == "참여하기":
            self.client = ClientUser()

    def create_button(self, text, x, y):
        font = pygame.font.Font(None, self.FONT_SIZE)
        text_surface = font.render(text, True, self.TEXT_COLOR)
        button_rect = pygame.Rect(x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect)
        self.screen.blit(text_surface, (x + (self.BUTTON_WIDTH - text_surface.get_width()) //
                         2, y + (self.BUTTON_HEIGHT - text_surface.get_height()) // 2))

    def display(self, main):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.server_button_rect.collidepoint(event.pos):
                    self.handle_button_click("Server")
                elif self.client_button_rect.collidepoint(event.pos):
                    self.handle_button_click("Client")

        self.screen.fill((0, 0, 0))

        # Calculate button positions
        total_button_width = (
            self.BUTTON_WIDTH + self.BUTTON_SPACING) * 2 - self.BUTTON_SPACING
        button_start_x = (self.screen.get_width() -
                          total_button_width) // 2

        # Create Server button
        self.server_button_rect = pygame.Rect(button_start_x, (self.screen.get_height(
        ) - self.BUTTON_HEIGHT) // 2, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.create_button(
            "Server", self.server_button_rect.x, self.server_button_rect.y)

        # Create Client button
        self.client_button_rect = pygame.Rect(button_start_x + self.BUTTON_WIDTH + self.BUTTON_SPACING, (
            self.screen.get_height() - self.BUTTON_HEIGHT) // 2, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.create_button(
            "Client", self.client_button_rect.x, self.client_button_rect.y)

        pygame.display.flip()
        self.clock.tick(60)
