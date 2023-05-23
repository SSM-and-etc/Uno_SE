import pygame
import numpy as np
from System.images import Images
from System.statebuttons import StateButtons
from System.texts import Texts
from System.esc_menu import EscMenu

# texts index
PLAYER0_NAME = 0; PLAYER1_NAME = 1; PLAYER2_NAME = 2; PLAYER3_NAME = 3; PLAYER4_NAME = 4; PLAYER5_NAME = 5
# ...이후는 초기값으로 문자열 고정
MAX_PLAYER_COUNT = 6


class SingleLobby():
    def __init__(self, main):
        self.main = main
        self.user_data = main.user_data
        self.BG = Images(main.user_data, main.root_path, (1280, 720))
        self.imgs = Images(main.user_data, main.root_path, (1280, 720))
        self.buttons = StateButtons(main.user_data, main.root_path, (1280, 720))
        self.texts = Texts(main.user_data)
        #self.ex_texts = Texts(main.user_data)
        
        self.on_esc = False
        
        self.esc = EscMenu(main, self)
        self.reset()
        self.add_assets()
        self.input_string_reset()
        self.imgs.set_checked(0, 0, True)
        self.ex_texts_counter = 0
        
    def display(self, main):
        self.draw(main.screen)
        if self.on_esc:
            self.on_esc = self.esc.display(main)
        else:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main.running = False
                        
                    if event.type == pygame.KEYDOWN:
                        self.keydown(main, event)
                    
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        self.click_collide(main, event.pos)
                        
                    if self.on_input_string and (not self.buttons.is_state_holding): # esc, 범위 외 클릭에 의한 string 입력상태 해제
                        self.apply_change_string()
                        
                    if event.type == pygame.MOUSEMOTION:
                        self.move_collide(main, event.pos)

                    if event.type == pygame.USEREVENT and self.ex_texts_counter > 0:
                        self.ex_texts_counter -= 1
    
    def draw(self, screen):
        self.BG.draw(screen)
        self.imgs.draw(screen)
        self.buttons.draw(screen)
        self.texts.draw(screen)
        if self.ex_texts_counter > 0:
            self.ex_texts.draw(screen)        
        
    def keydown(self, main, event):
        if self.on_input_string:
            if event.key == self.user_data.key_enter or event.key == pygame.K_ESCAPE:
                self.apply_change_string()
            else:
                self.write_string(event)
        elif not self.buttons.key_down_state(event.key):
            match event.key:
                case self.user_data.key_enter:
                    self.enter_state()
                case pygame.K_ESCAPE:
                    self.on_esc = True
                    
    def click_collide(self, main, mouse_pos):
        clicked_button_idx = self.buttons.get_clicked_button_idx(mouse_pos)
        if clicked_button_idx:
            self.enter_state()
            
    def enter_state(self):
        i, j = self.buttons.get_state()
        match j:
            case 0:
                self.ban_player(i)
            case 1:
                self.enter_write_state(i)
            case 6:
                match i:
                    case 4:
                        self.start_game()
                    case 5:
                        self.exit()
            case _: # 2~5 ai 설정
                self.set_ai_player(i, j - 2)
    
    def enter_write_state(self, i):
        if self.on_input_string:
            self.apply_change_string()
        else:
            self.buttons.is_state_holding = True
            self.on_input_string = True
            self.now_text_index = i
            self.now_input_string = self.texts.get_only_text(self.now_text_index)
        
    def write_string(self, event):
        if len(self.now_input_string) > 0 and event.key == pygame.K_BACKSPACE:
                self.now_input_string = self.now_input_string[:-1]
                self.texts.change_text(self.now_text_index, self.now_input_string)
        elif len(self.now_input_string) <= 10:
            match event.key:
                case self.user_data.key_enter:
                    self.apply_change_string()
                case _:
                    if event.unicode.isalnum():
                        self.now_input_string += event.unicode
                        self.texts.change_text(self.now_text_index, self.now_input_string)

    def move_collide(self, main, mouse_pos):
        clicked_button_idx = self.buttons.get_on_cursor_buttton_idx(mouse_pos)
        
    def add_assets(self):
        self.add_imgs()
        self.add_buttons()
        self.add_texts()
        
    def add_imgs(self):
        self.BG.add_row("Material/BG/white.png", "Material/ColorMode/BG/sky_blue.png", (0.5, 0.5))
        self.imgs.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs.add("Material/Button/Lobby/host.png", "Material/Button/Lobby/host.png", (0.225, 0))
        self.imgs.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs.add("Material/Button/Lobby/player1.png", "Material/Button/Lobby/player1.png", (0.225, 0))
        self.imgs.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs.add("Material/Button/Lobby/player2.png", "Material/Button/Lobby/player2.png", (0.225, 0))
        self.imgs.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs.add("Material/Button/Lobby/player3.png", "Material/Button/Lobby/player3.png", (0.225, 0))
        self.imgs.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs.add("Material/Button/Lobby/player4.png", "Material/Button/Lobby/player4.png", (0.225, 0))
        self.imgs.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs.add("Material/Button/Lobby/player5.png", "Material/Button/Lobby/player5.png", (0.225, 0))
        
        for i in range(2):
            self.imgs.set_col_linspace(i, 0.1, 1)
        
    def add_buttons(self):
        self.buttons.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons.add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons.add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons.add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons.add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons.add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/start_game.png", "Material/Button/Lobby/start_game.png", (0.89, 0.743))
        self.buttons.add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons.add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons.add("Material/Button/Lobby/exit_room.png", "Material/Button/Lobby/exit_room.png", (0.89, 0.871))
        
        for i in range(6):
            self.buttons.set_col_linspace(i, 0.1, 1)
        
        
    def add_texts(self):
        self.texts.add("", (0.33, 0.21), 40, "BLACK", "BLACK")
        self.texts.add("", (0.33, 0.339), 40, "BLACK", "BLACK")
        self.texts.add("", (0.33, 0.468), 40, "BLACK", "BLACK")
        self.texts.add("", (0.33, 0.597), 40, "BLACK", "BLACK")
        self.texts.add("", (0.33, 0.726), 40, "BLACK", "BLACK")
        self.texts.add("", (0.33, 0.855), 40, "BLACK", "BLACK")
        self.texts.add("ban", (0.02, 0.1), 40, "BLACK", "BLACK")
        self.texts.add("exist", (0.1, 0.1), 40, "BLACK", "BLACK")
        self.texts.add("name", (0.35, 0.1), 40, "BLACK", "BLACK")
        self.texts.add("StoryAI(0: default)", (0.57, 0.1), 40, "BLACK", "BLACK")
        
    def apply_screen_size(self):
        self.BG.apply_screen_size()
        # for i in range(len(self.imgs)):
        self.imgs.apply_screen_size()
        self.buttons.apply_screen_size()
        self.texts.apply_screen_size()
        
        self.esc.apply_screen_size()
        
    def change_screen_size(self):
        self.apply_screen_size()
        
    def reset(self):
        self.players_index        = [-1, -2, -2, -2, -2, -2] # -2: 빈 칸, -1: 유저, 0 ~ 4: 각 스테이지 ai(0은 defaultAI)
        self.possible_player_count = MAX_PLAYER_COUNT  # 최대 접속 가능 유저 수(닫힌 칸 제외)
        self.exist_player_count = 1     # 접속 유저 수(방장 포함)
        self.on_input_string = False
        self.now_input_string = ""
        self.now_text_index = 0
        
    def exit(self):
        self.reset()
        self.main.scene_change(self.main.get_scene_index("title"))
    
    def input_string_reset(self):
        self.set_default_name()
            
    def set_default_name(self):
        self.texts.change_text(0, "Host")
        for i in range(1, MAX_PLAYER_COUNT):
            if self.players_index[i] >= 0:
                self.texts.change_text(i, "AIPlayer" + str(i))
                
    def set_ai_default_name_all(self):
        for i in range(1, MAX_PLAYER_COUNT):
            if self.players_index >= 0:
                self.texts.change_text(i, "AiPlayer" + str(i))
                
    def set_ai_default_name(self, i):
        self.texts.change_text(i, "AiPlayer" + str(i))
                
        self.players_index[0] = -1
        self.imgs.set_checked(0, 0, True)
        self.set_default_name()
        
    def get_empty_seat_count(self):
        return self.possible_player_count - self.exist_player_count
    
    def ban_player(self, i): # i: 0(host), 1~5: 유저 or ai or 빈칸
        if i == 0:
            return
        if self.is_ai(i):
            self.set_ai_story_index(i)
            #TODO: i번쨰 AiPlayer 
        elif self.is_user(i):
            pass #TODO: i번째 유저 추방
        else:
            return
        
        self.room_member_exit(i)
        
    def is_ai(self, i):
        return self.players_index[i] >= 0
    
    def is_user(self, i):
        return self.players_index[i] == -1
    
    def set_exist_players(self):
        for i in range(MAX_PLAYER_COUNT):
            self.imgs.set_checked(i, 0, self.players_index[i] >= -1)
            
    def apply_change_string(self):
        self.on_input_string = False
        self.buttons.is_state_holding = False
                
    def room_member_exit(self, i):
        self.imgs.set_checked(i, 0, False)
        self.texts.change_text(i, "")
        self.possible_player_count += 1
        self.exist_player_count -= 1
        self.players_index[i] = -2
        
    def set_ai_player(self, i, story_index):
        if self.players_index[i] == -1 or self.user_data.story_level < story_index: # 플레이어 존재시, stage 레벨 부족시 ai 설정 불가
            return
        if self.players_index[i] == -2: # 빈칸일 경우
            self.set_ai_default_name(i)
            self.imgs.set_checked(i, 0, True)
            self.possible_player_count -= 1
            self.exist_player_count += 1
        self.set_ai_story_index(i, story_index)
        self.players_index[i] = story_index
        
    def start_game(self):
        if self.exist_player_count < 2:
            return
        self.process_game_start()
        self.main.scene_change(self.main.get_scene_index("game start"))
        
    def process_game_start(self):
        self.main.set_player_info(self.get_players_name_list(), self.players_index)
    
    def get_players_name_list(self):
        name_list = []
        for i in range(MAX_PLAYER_COUNT):
            name_list.append(self.texts.get_only_text(i))
        return name_list
            
    def set_ai_story_index(self, i, story_index = -1):
        for j in range(2, 6):
            self.buttons.set_checked(i, j, False)
        if story_index >= 0:
            self.buttons.set_checked(i, story_index + 2, True)