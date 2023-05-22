import pygame
import numpy as np
from System.images import Images
from System.statebuttons import StateButtons
from System.texts import Texts
from System.esc_menu import EscMenu

# texts[1] index
PW_STRING    = 0
# texts[2] index
IP_STRING    = 0
# texts[3] index
PW_STRING    = 0
# texts[4] index
PLAYER0_NAME = 0; PLAYER1_NAME = 1; PLAYER2_NAME = 2; PLAYER3_NAME = 3; PLAYER4_NAME = 4; PLAYER5_NAME = 5
IP_STRING    = 6
PW_STRING    = 7
# ...이후는 초기값으로 문자열 고정
MAX_PLAYER_COUNT = 6


class MultiLobby():
    def __init__(self, main):
        self.main = main
        self.user_data = main.user_data
        self.BG = Images(main.user_data, main.root_path, (1280, 720))
        self.imgs = [Images(main.user_data, main.root_path, (1280, 720)), Images(main.user_data, main.root_path, (1280, 720)), Images(main.user_data, main.root_path, (1280, 720)), Images(main.user_data, main.root_path, (1280, 720)), Images(main.user_data, main.root_path, (1280, 720))]
        self.buttons = [StateButtons(main.user_data, main.root_path, (1280, 720)), StateButtons(main.user_data, main.root_path, (1280, 720)), StateButtons(main.user_data, main.root_path, (1280, 720)), StateButtons(main.user_data, main.root_path, (1280, 720)), StateButtons(main.user_data, main.root_path, (1280, 720))]
        self.texts = [Texts(main.user_data), Texts(main.user_data), Texts(main.user_data), Texts(main.user_data), Texts(main.user_data)]
        self.ex_texts = Texts(main.user_data)
        
        self.on_esc = False
        
        self.esc = EscMenu(main, self)

        self.state = 0          # 0: 방만들기/참여, 1: 비밀번호설정, 방 만들기, 2: 방 참여, 3: 방 비밀번호 입력, 4: 로비
        self.reset()
        self.add_assets()
        self.input_string_reset()
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
                        
                    if not self.buttons[self.state].is_state_holding: # esc, 범위 외 클릭에 의한 string 입력상태 해제
                        self.on_input_string = False
                        
                    if event.type == pygame.MOUSEMOTION:
                        self.move_collide(main, event.pos)

                    if event.type == pygame.USEREVENT and self.ex_texts_counter > 0:
                        self.ex_texts_counter -= 1
    
    def draw(self, screen):
        self.BG.draw(screen)
        self.imgs[self.state].draw(screen)
        self.buttons[self.state].draw(screen)
        self.texts[self.state].draw(screen)
        if self.ex_texts_counter > 0:
            self.ex_texts.draw(screen)        
        
    def keydown(self, main, event):
        if self.on_input_string:
            self.write_string(event)
        if not self.buttons[self.state].key_down_state(event.key):
            match event.key:
                case self.user_data.key_enter:
                    self.enter_state()
                case pygame.K_ESCAPE:
                    self.on_esc = True
                    
    def click_collide(self, main, mouse_pos):
        clicked_button_idx = self.buttons[self.state].get_clicked_button_idx(mouse_pos)
        if clicked_button_idx:
            self.enter_state()
            
    def enter_state(self):
        match self.state:
            case 0:
                self.enter_state0()
            case 1:
                self.enter_state1()
            case 2:
                self.enter_state2()
            case 3:
                self.enter_state3()
            case 4:
                self.enter_state4()
        
    def enter_state0(self):
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                match j:
                    case 0:
                        self.state = 1
                    case 1:
                        self.state = 2
            case 1:
                self.exit()
        
    def enter_state1(self):
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                self.enter_write_state(0)
            case 1:
                self.create_lobby()
            case 2:
                self.exit()
                
        
    def enter_state2(self):
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                self.enter_write_state(0)
            case 1:
                self.check_lobby()
            case 2:
                self.exit()
        
    def enter_state3(self):
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                self.enter_write_state(0)
            case 1:
                self.check_pw()
            case 2:
                self.exit()
        
    def enter_state4(self):
        i, j = self.buttons[self.state].get_state()
        match j:
            case 0:
                match i:
                    case 0:
                        pass
        
    def enter_write_state(self, i):
        if self.on_input_string:
            self.on_input_string = False
            self.buttons[self.state].is_state_holding = False
        else:
            self.buttons[self.state].is_state_holding = True
            self.on_input_string = True
            self.now_text_index = i
            self.now_input_string = self.texts[self.state].get_only_text(self.now_text_index)
        
    def write_string(self, event):
        if len(self.now_input_string) > 0 and event.key == pygame.K_BACKSPACE:
                self.now_input_string = self.now_input_string[:-1]
                self.texts[self.state].change_text(self.now_text_index, self.now_input_string)
        elif len(self.now_input_string) <= 10:
            match event.key:
                case self.user_data.key_enter:
                    self.on_input_string = False
                case _:
                    if event.unicode.isalnum():
                        self.now_input_string += event.unicode
                        self.texts[self.state].change_text(self.now_text_index, self.now_input_string)

    def move_collide(self, main, mouse_pos):
        clicked_button_idx = self.buttons[self.state].get_on_cursor_buttton_idx(mouse_pos)
        
    def add_assets(self):
        self.add_imgs()
        self.add_buttons()
        self.add_texts()
        
    def add_imgs(self):
        self.BG.add_row("Material/BG/white.png", "Material/ColorMode/BG/sky_blue.png", (0.5, 0.5))
        self.imgs[0].add_row("Material/GUI/pop_up.png", "Material/ColorMode/GUI/pop_up.png", (0.5, 0.5))
        self.imgs[1].add_row("Material/GUI/pop_up.png", "Material/ColorMode/GUI/pop_up.png", (0.5, 0.5))
        self.imgs[2].add_row("Material/GUI/pop_up.png", "Material/ColorMode/GUI/pop_up.png", (0.5, 0.5))
        self.imgs[3].add_row("Material/GUI/pop_up.png", "Material/ColorMode/GUI/pop_up.png", (0.5, 0.5))
        self.imgs[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs[4].add("Material/Button/Lobby/host.png", "Material/Button/Lobby/host.png", (0.225, 0))
        self.imgs[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs[4].add("Material/Button/Lobby/player1.png", "Material/Button/Lobby/player1.png", (0.225, 0))
        self.imgs[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs[4].add("Material/Button/Lobby/player2.png", "Material/Button/Lobby/player2.png", (0.225, 0))
        self.imgs[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs[4].add("Material/Button/Lobby/player3.png", "Material/Button/Lobby/player3.png", (0.225, 0))
        self.imgs[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs[4].add("Material/Button/Lobby/player4.png", "Material/Button/Lobby/player4.png", (0.225, 0))
        self.imgs[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.125, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.imgs[4].add("Material/Button/Lobby/player5.png", "Material/Button/Lobby/player5.png", (0.225, 0))
        
        for i in range(2):
            self.imgs[4].set_col_linspace(i, 0.1, 1)
        
    def add_buttons(self):
        self.buttons[0].add_row("Material/Button/Lobby/create_lobby.png", "Material/Button/Lobby/create_lobby.png", (0.5, 0.5))
        self.buttons[0].add("Material/Button/Lobby/enter_lobby.png", "Material/Button/Lobby/enter_lobby.png", (0.5, 0.5))
        self.buttons[0].set_row_linspace(0, 0.1, 0.9)
        self.buttons[0].add_row("Material/Button/Lobby/back.png", "Material/Button/Lobby/back.png", (0.75, 0.2))
        self.buttons[1].add_row("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.55, 0.4))
        self.buttons[1].add_row("Material/Button/Lobby/create_lobby.png", "Material/Button/Lobby/create_lobby.png", (0.5, 0.65))
        self.buttons[1].add_row("Material/Button/Lobby/back.png", "Material/Button/Lobby/back.png", (0.75, 0.2))
        self.buttons[2].add_row("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.55, 0.4))
        self.buttons[2].add_row("Material/Button/Lobby/enter_lobby.png", "Material/Button/Lobby/enter_lobby.png", (0.5, 0.65))
        self.buttons[2].add_row("Material/Button/Lobby/back.png", "Material/Button/Lobby/back.png", (0.75, 0.2))
        self.buttons[3].add_row("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.55, 0.4))
        self.buttons[3].add_row("Material/Button/Lobby/enter_lobby.png", "Material/Button/Lobby/enter_lobby.png", (0.5, 0.65))
        self.buttons[3].add_row("Material/Button/Lobby/back.png", "Material/Button/Lobby/back.png", (0.75, 0.2))
       
        self.buttons[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons[4].add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0), "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.96, 0.225))
        self.buttons[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons[4].add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons[4].add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons[4].add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons[4].add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/start_game.png", "Material/Button/Lobby/start_game.png", (0.89, 0.743))
        self.buttons[4].add_row("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.05, 0), "Material/Button/Lobby/ban_box.png", "Material/Button/Lobby/ban_box.png")
        self.buttons[4].add("Material/Button/Lobby/string_bar.png", "Material/Button/Lobby/string_bar.png", (0.43, 0))
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.6, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.65, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.7, 0),  "Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/box.png", "Material/Button/Lobby/box.png", (0.75, 0),"Material/Button/Lobby/check_box.png", "Material/Button/Lobby/check_box.png")
        self.buttons[4].add("Material/Button/Lobby/exit_room.png", "Material/Button/Lobby/exit_room.png", (0.89, 0.871))
        
        for i in range(6):
            self.buttons[4].set_col_linspace(i, 0.1, 1)
        
        
    def add_texts(self):
        self.texts[1].add("", (0.45, 0.36), 40, "arial", "BLACK", "BLACK")
        self.texts[1].add("PW: ", (0.32, 0.37), 40, "arial", "BLACK", "BLACK")
        self.texts[2].add("", (0.45, 0.36), 40, "arial", "BLACK", "BLACK") 
        self.texts[2].add("IP: ", (0.32, 0.37), 40, "arial", "BLACK", "BLACK")
        self.texts[3].add("", (0.45, 0.36), 40, "arial", "BLACK", "BLACK") 
        self.texts[3].add("PW: ", (0.32, 0.37), 40, "arial", "BLACK", "BLACK")
        
        self.texts[4].add("", (0.33, 0.21), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.33, 0.339), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.33, 0.468), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.33, 0.597), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.33, 0.726), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.33, 0.855), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.82, 0.1), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.82, 0.21), 40, "BLACK", "BLACK")
        self.texts[4].add("IP: ", (0.78, 0.1), 40, "BLACK", "BLACK")
        self.texts[4].add("PW: ", (0.78, 0.21), 40, "BLACK", "BLACK")
        self.texts[4].add("ban", (0.02, 0.1), 40, "BLACK", "BLACK")
        self.texts[4].add("exist", (0.1, 0.1), 40, "BLACK", "BLACK")
        self.texts[4].add("name", (0.35, 0.1), 40, "BLACK", "BLACK")
        self.texts[4].add("StoryAI(0: default)", (0.57, 0.1), 40, "BLACK", "BLACK")
        self.ex_texts.add("", (0.3, 0.07), 20, "arial")
        
    def apply_screen_size(self):
        self.BG.apply_screen_size()
        # for i in range(len(self.imgs)):
        for i in range(5):
            self.imgs[i].apply_screen_size()
            self.buttons[i].apply_screen_size()
            self.texts[i].apply_screen_size()
        self.ex_texts.apply_screen_size()
        
        self.esc.apply_screen_size()
        
    def change_screen_size(self):
        self.apply_screen_size()
        
    def reset(self):
        self.is_server = False
        self.lobby_index = -1   # 0: 방장, 1 ~ 5: 참가 유저
        self.possible_invite = [False, False, False, False, False, False] # 각 자리에 접속 가능 여부
        self.ai_index        = [-1, -1, -1, -1, -1, -1] # -1: 유저, 0 ~ 4: 각 스테이지 ai(0은 defaultAI)
        self.possible_player_count = 0  # 최대 접속 가능 유저 수(닫힌 칸 제외)
        self.exist_player_count = 0     # 접속 유저 수(방장 포함)
        self.on_input_string = False
        self.now_input_string = ""
        self.now_text_index = 0
        self.room_password = ""
        
    def exit(self):
        self.reset()
        self.input_string_reset()
        match self.state:
            case 0:
                self.main.scene_change(self.main.get_scene_index("title"))
            case 1:
                self.state = 0
            case 2:
                self.state = 0
            case 3:
                self.state = 2
            case 4:
                self.state = 1
    
    def input_string_reset(self):
        for i in range(1, 4):
            self.texts[i].change_text(0, "")
        self.set_default_name()
        for i in range(MAX_PLAYER_COUNT, PW_STRING + 1):
            self.texts[4].change_text(i, "")
            
    def set_default_name(self):
        self.texts[4].change_text(0, "Host")
        for i in range(1, MAX_PLAYER_COUNT):
            self.texts[4].change_text(i, "Player" + str(i))
        self.texts[4].change_text(IP_STRING, self.get_my_ip())
        self.texts[4].change_text(PW_STRING, self.room_password)
                
    def set_ai_default_name(self):
        for i in range(1, MAX_PLAYER_COUNT):
            if self.ai_index >= 0:
                self.texts[4].change_text(i, "AiPlayer" + str(i))
                
    def set_pw(self, pw):
        self.room_password = pw
        
    def get_pw(self):
        return self.room_password
    
    def create_lobby(self):  #TODO: 방장의 로비 생성, 소켓 관련 연결, 
        self.state = 4
        self.change_pw(self.now_input_string)
        self.set_default_name()
        
    def check_lobby(self):  #TODO: ip주소로 방 접속 가능 여부 확인(1: 빈자리 여부(없으면 오류 메시지, 있으면 2로), 2: 비밀번호 여부 검사(있으면 self.state = 3설정, 비밀번호 입력 화면으로 이동 3으로, 없으면 self.state = 4 설정 후 로비 접속)
        if True:                # 로비의 빈자리 확인 (방장의 self.)
            if False:            # 로비의 비밀번호 없는지 확인
                self.enter_lobby()
            else:
                self.state = 3  # 비밀번호 입력 화면으로 이동
        else:
            self.ex_texts.change_text(0, "The room is full.")
            self.ex_texts_counter = 3
            pygame.time.set_timer(pygame.USEREVENT, 1000)
                
    def enter_lobby(self):  #TODO: 방 참가, 소켓 관련 연결
        self.state = 4
        
        # 참가하고자 입력했던 방의 ip
    def get_input_ip(self):
        return self.texts[2].get_only_text(0)
    
    def get_my_ip(self): #TODO: 자기 IP 반환
        return "12.34.56.78"
    
    def get_empty_seat(self):
        return self.possible_player_count - self.exist_player_count
    
    def check_pw(self):     # 방의 비밀번호와 맞는지 확인
        ip = self.get_input_ip()
        # pw = 방의 비밀번호
        #if self.now_input_string == pw:
        if True:
            self.enter_lobby()
        else:
            self.ex_texts.change_text(0, "Invalid password.")
            self.ex_texts_counter = 3
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            
    def change_pw(self, pw): # 방 비밀번호 변경시 처리
        self.room_password = pw
        