import pygame

from MultiLobby.server_user import ServerUser
from MultiLobby.client_user import ClientUser

z
class MultiLobby:
    def __init__(self, main):
        self.WHITE = (255, 255, 255)
        self.ORANGE = (255, 163, 0)
        self.clock = pygame.time.Clock()
        self.lobby_img = pygame.image.load("Material/BG/Title.png")

        self.ratio_list = [(0.8, 0.05), (0.8, 0.2), (0.8, 0.35),
                           (0.8, 0.5), (0.8, 0.65), (0.8, 0.8)]
        self.original_size = self.lobby_img.get_rect().size
        self.screen = main.screen
        self.screen_width = main.screen.get_width()
        self.screen_heigth = main.screen.get_height()

        self.aspect_ratio = self.screen_width / 1280, self.screen_heigth / 720
        self.new_width = int(self.original_size[0] * self.aspect_ratio[0])
        self.new_height = int(self.original_size[1] * self.aspect_ratio[1])
        self.lobby_img = pygame.transform.scale(
            self.lobby_img, (self.new_width, self.new_height))
        self.font = pygame.font.Font(None, int(self.screen_width/30))
        # self.make_screen(self.screen_width,
        #                  self.screen_heigth, self.ratio_list)
        self.mouse_pos = pygame.mouse.get_pos()

        # self.check_user
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
        if button_name == "Server":
            self.server = ServerUser(self)
            self.server.run()
        elif button_name == "Client":
            self.client = ClientUser(self)
            self.client.run()

    def create_button(self, text, x, y):
        font = self.font
        text_surface = font.render(text, True, self.ORANGE)
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

        main.screen.blit(self.lobby_img, (0, 0))

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
