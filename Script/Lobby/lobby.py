import pygame

from Lobby.input_box import InputBox
from Lobby.button import StartButton


class Lobby():
    def __init__(self, main):
        self.WHITE = (255, 255, 255)
        self.ORANGE = (255, 163, 0)
        self.lobby_img = pygame.image.load("Material/BG/Title.png")
        self.ratio_list = [(0.8, 0.05), (0.8, 0.2), (0.8, 0.35),
                           (0.8, 0.5), (0.8, 0.65), (0.8, 0.8)]
        self.original_size = self.lobby_img.get_rect().size
        self.player_box_info = []
        self.player_list = []
        self.screen = main.screen
        self.screen_width = main.screen.get_width()
        self.screen_heigth = main.screen.get_height()
        self.aspect_ratio = self.screen_width / 1280, self.screen_heigth / 720
        self.new_width = int(self.original_size[0] * self.aspect_ratio[0])
        self.new_height = int(self.original_size[1] * self.aspect_ratio[1])
        self.lobby_img = pygame.transform.scale(
            self.lobby_img, (self.new_width, self.new_height))
        self.font = pygame.font.Font(None, int(self.screen_width/30))
        self.make_screen(self.screen_width,
                         self.screen_heigth, self.ratio_list)
        self.mouse_pos = pygame.mouse.get_pos()
        self.start_button = StartButton("Start", self.screen_width*0.4, self.screen_heigth*0.6,
                                        self.screen_width/6, self.screen_heigth/10, self.ORANGE, self.font, self.screen, self.check_user)
        self.play_game
        self.check_user
        self.main = main
        self.index = -1
        self.count = 0
        for i, info in enumerate(self.player_box_info):
            self.player_list.append(
                InputBox(info[0], info[1], info[2], info[3], i, 'player'+str(i), self.font))

    def display(self, main):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start_button.handle_event(event)
            for computer in self.player_list:
                computer.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.index -= 1
                if event.key == pygame.K_DOWN:
                    self.index += 1

                if (self.index < -1):
                    self.index = 5
                if (self.index > 5):
                    self.index = -1
                if (self.index > -1):
                    self.player_list[self.index].handle_key_event(
                        event, self.index)

                if event.key == pygame.K_RETURN:
                    if (self.index == -1):
                        self.start_button.handle_key_event(event)

        main.screen.blit(self.lobby_img, (0, 0))
        for computer in self.player_list:
            computer.draw(main.screen)
        self.start_button.draw()

    def make_screen(self, width, height, ratios):
        for ratio in ratios:
            self.player_box_info.append(
                (width*ratio[0], height*ratio[1], self.screen_width/6, self.screen_heigth/12))

    def check_user(self):
        for user in self.player_list:
            if user.clicked == True:
                self.count += 1
        if self.count > 1:
            self.play_game()
        else:
            self.count = 0

    def play_game(self):
        self.main.add_info(self.player_list)
        self.main.scene_change(self.main.get_scene_index("game start"))

    def change_screen_size(self):
        pass  # title의 size 변경 방식과의 호환을 위해 임시로 만듦
