import pygame

import os

# Constants
STATE_NUMBER = 3
STATE_SINGLE_GAME = 0
STATE_OPTION = 1
STATE_EXIT = 2

class Title():
    def __init__(self, root, screen_size):
        self.title_BG = pygame.image.load(os.path.join(root, "Material/BG/title.png"))
        self.single_game_img = pygame.image.load(os.path.join(root, "Material/Button/single_game.png"))
        self.option_img = pygame.image.load(os.path.join(root, "Material/Button/option.png"))
        self.exit_img = pygame.image.load(os.path.join(root, "Material/Button/exit.png"))
        self.button_select_img = pygame.image.load(os.path.join(root, "Material/Button/button_select.png"))

        self.single_game_default_pos = (0.2, 0.7)
        self.option_default_pos = (0.6, 0.7)
        self.exit_default_pos = (0.8, 0.7)
        
        self.on_title_gui = True
        self.select_state = 0 # 0: single game start, 1: option, 2: exit ...
        
        self.set_title_gui(screen_size)
        self.apply_state_change()
        
    def display(self, main, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False
                
            if event.type == pygame.KEYDOWN:
                self.keydown_title(main, event.key)
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                self.collide_title(main, event.pos)
                
            if event.type == pygame.MOUSEMOTION:
                pass
            
        screen.blit(self.title_BG, (0, 0))
        if(self.on_title_gui):
            self.draw_title(screen)
            
    def draw_title(self, screen):
        screen.blit(self.single_game_img, self.single_game_rect)
        screen.blit(self.option_img, self.option_rect)
        screen.blit(self.exit_img, self.exit_rect)
        
    def collide_title(self, main, mouse_pos):
        if(self.single_game_rect.collidepoint(mouse_pos)):
            # TODO: 싱글 게임 시작 호출
            pass
        elif(self.option_rect.collidepoint(mouse_pos)):
            self.on_title_gui = False
            # TODO: 옵션창 호출
        elif (self.self.exit_rect.collidepoint(mouse_pos)):
            main.running = False
            
    def keydown_title(self, main, key):
        if(key == main.user_data.key_left):
            self.select_state -= 1
            while(self.select_state < 0):
                self.select_state += STATE_NUMBER
        elif(key == main.user_data.key_right):
            self.select_state += 1
            while(self.select_state >= STATE_NUMBER):
                self.select_state -= STATE_NUMBER
        elif(key == main.user_data.key_enter):
            self.enter_state(main)
            return
        else:
            # 사용 가능한 키 보여주기
            return
        
        self.apply_state_change()
            
    def apply_state_change(self):
        # TODO: 현재 state에 따라 select 이미지 적절하게 이동시키기
        pass
    
    def enter_state(self, main):
        if(self.select_state == STATE_SINGLE_GAME):
            # TODO: 싱글 게임 시작 호출 
            pass
        elif(self.select_state == STATE_OPTION):
            self.on_title_gui = False
            # TODO: 옵션창 호출
            pass
        elif(self.select_state == STATE_EXIT):
            main.running = False
        
    
    def set_title_gui(self, screen_size):
        self.single_game_pos = self.tup_mul(screen_size, self.single_game_default_pos)
        self.option_pos = self.tup_mul(screen_size, self.option_default_pos)
        self.exit_pos = self.tup_mul(screen_size, self.exit_default_pos)
        
        self.single_game_rect = self.single_game_img.get_rect(center = self.single_game_pos)
        self.option_rect = self.option_img.get_rect(center = self.option_pos)
        self.exit_rect = self.exit_img.get_rect(center = self.exit_pos)
        
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])
    
    