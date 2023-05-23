import pygame
import numpy as np
from System.images import Images
from System.statebuttons import StateButtons
from System.texts import Texts
from System.esc_menu import EscMenu

import socket
import pickle

# texts[1] index
PW_STRING    = 0
# texts[2] index
IP_STRING    = 0
# texts[3] index
PW_STRING    = 0
# texts[4] index
PLAYER0_NAME = 0; PLAYER1_NAME = 1; PLAYER2_NAME = 2; PLAYER3_NAME = 3; PLAYER4_NAME = 4; PLAYER5_NAME = 5
PW_STRING    = 6
IP_STRING    = 7
# ...이후는 초기값으로 문자열 고정
MAX_PLAYER_COUNT = 6

PORT = 11223


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

        self.is_server = False

    def socket_handle(self):
        if self.is_server and self.state == 4:
            try:
                client = self.sock.accept()
                print(client)
                client[0].setblocking(0)

                self.sockets.append(client[0])
                self.players.append("")

                client[0].send(pickle.dumps({
                    "action": "ASK_PASSWORD",
                    "payload": {
                        "full": False, # TODO: Full check
                        "password": (self.get_pw() != ""),
                    }
                }))
            except:
                pass

            for i, sock in enumerate(self.sockets[1:]):
                idx = i+1
                try:
                    data = pickle.loads(sock.recv(4096))
                    print("SERVER: ", data)

                    if data["action"] == "CHECK_PASSWORD":
                        if data["payload"]["password"] == self.get_pw():
                            self.players[idx] = f"Player{len(self.players)-1}"

                            sock.send(pickle.dumps({
                                "action": "JOIN", 
                                "payload": {
                                    "state": True,
                                    "players": self.players,
                                    "player": idx
                                }
                            }))
                            self.players_updated()

                        else:
                            sock.send(pickle.dumps({
                                "action": "JOIN",
                                "payload": {
                                    "state": False,
                                    "code": "WRONG_PASSWORD"
                                }
                            }))

                    elif data["action"] == "CHANGE_NAME":
                        self.players[idx] = data["payload"]
                        self.players_updated()
                
                except:
                    pass

        elif not self.is_server and self.state == 4:
            try:
                data = pickle.loads(self.server.recv(4096))

                print("CLIENT:", data)

                if data["action"] == "UPDATE_PLAYERS":
                    self.players = data["payload"]["players"]
                    self.players_updated()

                elif data["action"] == "GAME_START":
                    self.start_game_client()

                elif data["action"] == "BANNED":
                    self.state = 0
                    self.exit()
                    self.ex_text_print("you have been banished.")
                    # TODO: Notice you are banned 
                
            except:
                pass

    def ex_text_print(self, text):
        self.ex_texts.change_text(0, text)
        self.ex_texts_counter = 3
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def players_updated(self):
        print(self.players)
        for i in range(MAX_PLAYER_COUNT):
            if i < len(self.players):
                self.texts[4].change_text(i, self.players[i])
                self.imgs[4].set_checked(i, 0, True)
                #self.player_info[i] = -1
            else:
                self.texts[4].change_text(i, "")
                self.imgs[4].set_checked(i, 0, False)
                #self.player_info[i] = -2

        if self.is_server:
            for sock in filter(None, self.sockets):
                sock.send(pickle.dumps({
                    "action": "UPDATE_PLAYERS",
                    "payload": {
                        "players": self.players
                    }
                }))
        else:
            pass

        
    def display(self, main):
        self.socket_handle()
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
                        
                    if self.on_input_string and (not self.buttons[self.state].is_state_holding): # esc, 범위 외 클릭에 의한 string 입력상태 해제
                        self.apply_change_string()
                        
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
            if event.key == self.user_data.key_enter or event.key == pygame.K_ESCAPE:
                self.apply_change_string()
            else:
                self.write_string(event)
        elif not self.buttons[self.state].key_down_state(event.key):
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
        
    def enter_state0(self): # 방 만들기, 참여 창
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                match j:
                    case 0:
                        self.state = 1
                        self.is_server = True
                    case 1:
                        self.state = 2
                        self.is_server = False
            case 1:
                self.exit()
        
    def enter_state1(self): # 방 생성, 비밀번호 설정 창
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                self.enter_write_state(0)
            case 1:
                self.create_lobby()
            case 2:
                self.exit()
                
        
    def enter_state2(self): # 방 참가, ip 입력창
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                self.enter_write_state(0)
            case 1:
                self.check_lobby()
            case 2:
                self.exit()
        
    def enter_state3(self): # 방 참가, pw 입력창
        i, j = self.buttons[self.state].get_state()
        match i:
            case 0:
                self.enter_write_state(0)
            case 1:
                self.check_pw()
            case 2:
                self.exit()
        
    def enter_state4(self): # 로비 창
        if self.is_server:
            self.enter_stage4_host()
        else:
            self.enter_stage4_member()
                
    def enter_stage4_host(self):
        i, j = self.buttons[self.state].get_state()
        match j:
            case 0:
                self.ban_player(i)
            case 1:
                if i == self.lobby_index or self.is_ai(i):
                    self.enter_write_state(i)
            case 6:
                match i:
                    case 0: # pw 변경
                        self.enter_write_state(j)
                    case 4:
                        self.start_game()
                    case 5:
                        self.exit()
            case _: # 2~5 ai 설정
                self.set_ai_player(i, j - 2)
    
    def enter_stage4_member(self):
        i, j = self.buttons[self.state].get_state()
        match j:
            case 1:
                if i == self.lobby_index:
                    self.enter_write_state(i)
            case 6:
                match i:
                    case 5:
                        self.exit()
            
        
    def enter_write_state(self, i):
        if self.on_input_string:
            self.apply_change_string()
        else:
            self.buttons[self.state].is_state_holding = True
            self.on_input_string = True
            self.now_text_index = i
            self.now_input_string = self.texts[self.state].get_only_text(self.now_text_index)
        
    def write_string(self, event):
        if len(self.now_input_string) > 0 and event.key == pygame.K_BACKSPACE:
                self.now_input_string = self.now_input_string[:-1]
                self.texts[self.state].change_text(self.now_text_index, self.now_input_string)
        elif len(self.now_input_string) <= 16:
            match event.key:
                case self.user_data.key_enter:
                    self.apply_change_string()
                case _:
                    if event.unicode.isprintable():
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
        self.texts[4].add("", (0.82, 0.21), 40, "BLACK", "BLACK")
        self.texts[4].add("", (0.82, 0.1), 40, "BLACK", "BLACK")
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
        self.lobby_index = -1   # 0: 방장, 1 ~ 5: 참가 유저
        self.possible_invite = [False, False, False, False, False, False] # 각 자리에 접속 가능 여부
        self.players_index        = [-2, -2, -2, -2, -2, -2] # -2: 빈 칸, -1: 유저, 0 ~ 4: 각 스테이지 ai(0은 defaultAI)
        self.possible_player_count = MAX_PLAYER_COUNT  # 최대 접속 가능 유저 수(닫힌 칸 제외)
        self.exist_player_count = 1     # 접속 유저 수(방장 포함)
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
                self.room_exit()
        self.is_server = False
    
    def input_string_reset(self):
        for i in range(1, 4):
            self.texts[i].change_text(0, "")
        self.set_default_name()
        for i in range(MAX_PLAYER_COUNT, PW_STRING + 1):
            self.texts[4].change_text(i, "")
            
    def set_default_name(self):
        self.texts[4].change_text(0, "Host")
        for i in range(1, MAX_PLAYER_COUNT):
            if self.players_index[i] >= 0:
                self.texts[4].change_text(i, "Player" + str(i))
        self.texts[4].change_text(IP_STRING, self.get_my_ip())
        self.texts[4].change_text(PW_STRING, self.room_password)
                
    def set_ai_default_name_all(self):
        for i in range(1, MAX_PLAYER_COUNT):
            if self.players_index >= 0:
                self.texts[4].change_text(i, "AiPlayer" + str(i))
                
    def set_ai_default_name(self, i):
        self.texts[4].change_text(i, "AiPlayer" + str(i))
                
    def set_pw(self, pw):
        self.room_password = pw
        
    def get_pw(self):
        return self.room_password
    
    def create_lobby(self):  #TODO: 방장의 로비 생성, 소켓 관련 연결, 
        self.state = 4
        self.lobby_index = 0
        self.players_index[0] = -1
        self.imgs[4].set_checked(0, 0, True)
        self.change_pw(self.now_input_string)
        self.set_default_name()

        self.sockets = [None]
        self.players = ["Host"]
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", PORT))
        self.sock.listen()
        self.sock.setblocking(0)

    def check_lobby(self):  #TODO: ip주소로 방 접속 가능 여부 확인(1: 빈자리 여부(없으면 오류 메시지, 있으면 2로), 2: 비밀번호 여부 검사(있으면 self.state = 3설정, 비밀번호 입력 화면으로 이동 3으로, 없으면 self.state = 4 설정 후 로비 접속)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.get_input_ip(), PORT))

        data = pickle.loads(self.server.recv(4096))

        assert data["action"] == "ASK_PASSWORD"

        if data["payload"]["full"] == False:                # 로비의 빈자리 확인 (방장의 self.)
            if data["payload"]["password"] == False:            # 로비의 비밀번호 없는지 확인
                self.server.send(pickle.dumps({
                    "action": "CHECK_PASSWORD",
                    "payload": {
                        "password": ""
                    }
                }))

                data = pickle.loads(self.server.recv(4096))

                assert data["action"] == "JOIN"

                if data["payload"]["state"]:
                    self.players = data["payload"]["players"]
                    self.lobby_index = data["payload"]["player"]
                    self.players_updated()
                    self.server.setblocking(0)
                    self.enter_lobby()
            else:
                self.state = 3  # 비밀번호 입력 화면으로 이동
        else:
            self.ex_texts.change_text(0, "The room is full.")
            self.ex_texts_counter = 3
            pygame.time.set_timer(pygame.USEREVENT, 1000)
                
    def enter_lobby(self):  #TODO: 방 참가, 소켓 관련 연결, 방에서의 번호(1~5) self.lobby_index에 저장해주기
        self.state = 4
        
        # 참가하고자 입력했던 방의 ip
    def get_input_ip(self):
        return self.texts[2].get_only_text(0)
    
    def get_my_ip(self): #TODO: 자기 IP 반환
        try:
            return socket.gethostbyname_ex(socket.gethostname())[-1][-1]
        except:
            return ""
    
    def get_empty_seat_count(self):
        return self.possible_player_count - self.exist_player_count
    
    def get_empty_set_index(self): # 빈 자리의 index 반환(1 ~ 5)
        for i in MAX_PLAYER_COUNT:
            if self.players_index[i] == -2:
                return i
        return -1 # error
            
    
    def check_pw(self):     # 방의 비밀번호와 맞는지 확인
        self.server.send(pickle.dumps({
            "action": "CHECK_PASSWORD",
            "payload": {
                "password": self.now_input_string
            }
        }))

        data = pickle.loads(self.server.recv(4096))

        assert data["action"] == "JOIN"

        if data["payload"]["state"]:
            self.players = data["payload"]["players"]
            self.lobby_index = data["payload"]["player"]
            self.players_updated()
            self.server.setblocking(0)
            self.enter_lobby()
        else:
            self.ex_texts.change_text(0, "Invalid password.")
            self.ex_texts_counter = 3
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            
    def change_pw(self, pw): # 방 비밀번호 변경시 처리
        self.room_password = pw
        
    def ban_player(self, i): # i: 0(host), 1~5: 유저 or ai or 빈칸
        if i == 0:
            return
        
        self.sockets[i].send(pickle.dumps({
            "action": "BANNED",
            "payload": ""
        }))
        self.sockets[i].close()
        self.players.pop(i)
        self.sockets.pop(i)
        self.ex_text_print("Player"+str(i)+" has been kicked out.")

        self.players_updated()

        '''
        if self.is_ai(i):
            self.set_ai_story_index(i)
            #TODO: i번쨰 AiPlayer 
        elif self.is_user(i):
            pass #TODO: i번째 유저 추방
        else:
            return
        
        self.room_member_exit(i)
        '''
        
    def is_ai(self, i):
        return self.players_index[i] >= 0
    
    def is_user(self, i):
        return self.players_index[i] == -1
    
    def set_exist_players(self):
        for i in range(MAX_PLAYER_COUNT):
            self.imgs[4].set_checked(i, 0, self.players_index[i] >= -1)
            
    def apply_change_string(self):
        self.on_input_string = False
        if self.state == 4:
            self.buttons[4].is_state_holding = False
            if self.now_text_index < MAX_PLAYER_COUNT:  #TODO: i번째 유저가 닉네임 변경, 변경한 이름은 self.now_input_string에 존재
                self.now_input_string

                if self.is_server:
                    self.players[0] = self.now_input_string
                    self.players_updated()

                else:
                    self.server.send(pickle.dumps({
                        "action": "CHANGE_NAME",
                        "payload": self.now_input_string
                    }))

            elif self.now_text_index == PW_STRING:      #TODO: 방 비밀번호 변경 적용
                self.room_password = self.now_input_string
                
    def room_exit(self):
        if self.is_server: # TODO: 방장이 방 폭파
            pass
        else: # TODO: 참여 멤버가 방에서 나감, 호스트한테 알리기
            pass
        self.state = 0
        
    def room_member_exit(self, i): # TODO: 멤버 한 명이 나갔음(팅김, 자기가 나감)을 확인한 경우 host가 호출해주기
        self.imgs[4].set_checked(i, 0, False)
        self.texts[4].change_text(i, "")
        self.possible_player_count += 1
        self.exist_player_count -= 1
        self.players_index[i] = -2
        
    def set_ai_player(self, i, story_index):
        if self.players_index[i] == -1 or self.user_data.story_level < story_index: # 플레이어 존재시, stage 레벨 부족시 ai 설정 불가
            return
        if self.players_index[i] == -2: # 빈칸일 경우
            self.set_ai_default_name(i)
            self.imgs[4].set_checked(i, 0, True)
            self.possible_player_count -= 1
            self.exist_player_count += 1
        self.set_ai_story_index(i, story_index)
        self.players_index[i] = story_index
        
    def start_game(self):
        #if self.exist_player_count < 2:
        #    return
        # TODO 멀티게임 시작

        for sock in filter(None, self.sockets):
            sock.send(pickle.dumps({
                "action": "GAME_START",
                "payload": "",
            }))

        self.main.sock = self.sock
        self.main.sockets = self.sockets

        self.main.players_name = self.players
        while len(self.main.sockets) < len(self.players):
            self.main.sockets.append(None)

        self.main.scene_change(self.main.get_scene_index("multi game server"))

    def start_game_client(self):
        self.main.server = self.server
        self.main.scene_change(self.main.get_scene_index("multi game client"))
        
    def process_game_start(self):
        self.main.set_player_info(self.get_players_name_list(), self.players_index)
    
    def get_players_name_list(self):
        name_list = []
        for i in range(MAX_PLAYER_COUNT):
            name_list.append(self.texts[4].get_only_text(i))
        return name_list
            
    def set_ai_story_index(self, i, story_index = -1):
        for j in range(2, 6):
            self.buttons[4].set_checked(i, j, False)
        if story_index >= 0:
            self.buttons[4].set_checked(i, story_index + 2, True)