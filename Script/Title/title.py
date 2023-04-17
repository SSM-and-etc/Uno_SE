import pygame

import os

from System.option import Option

# Constants
STATE_NUMBER = 3
STATE_SINGLE_GAME = 0
STATE_OPTION = 1
STATE_EXIT = 2

class Title():
    def __init__(self, main):
        self.main = main
        self.design_size = (1280, 720)
        
        self.default_title_BG = pygame.image.load(os.path.join(main.root_path, "Material/BG/title.png"))
        self.default_single_game_img = pygame.image.load(os.path.join(main.root_path, "Material/Button/single_game.png"))
        self.default_option_img = pygame.image.load(os.path.join(main.root_path, "Material/Button/option.png"))
        self.default_exit_img = pygame.image.load(os.path.join(main.root_path, "Material/Button/exit.png"))
        self.default_button_select_img = pygame.image.load(os.path.join(main.root_path, "Material/Button/button_select.png"))

        self.set_gui_default_pos()
        
        self.on_option = False
        self.select_state = 0 # 0: single game start, 1: option, 2: exit ...
        
        self.user_data = main.user_data
        self.option = Option(main, self)
        
        self.set_title_gui(self.user_data.get_screen_size())
        
    def display(self, main):
        if self.on_option:
            self.on_option = self.option.display(main)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main.running = False
                    
                if event.type == pygame.KEYDOWN:
                    self.keydown_title(main, event.key)
                
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.click_collide_title(main, event.pos)
                    
                if event.type == pygame.MOUSEMOTION:
                    self.move_collide_title(main, event.pos)
                    
            self.draw_title(main.screen)
            
    def draw_title(self, screen):
        screen.blit(self.title_BG, (0, 0))
        screen.blit(self.single_game_img, self.single_game_rect)
        screen.blit(self.option_img, self.option_rect)
        screen.blit(self.exit_img, self.exit_rect)
        screen.blit(self.button_select_img, self.button_select_rect)
        
    def click_collide_title(self, main, mouse_pos):
        if self.single_game_rect.collidepoint(mouse_pos):
            self.enter_state(main)
        elif self.option_rect.collidepoint(mouse_pos):
            self.on_option = True
        elif self.exit_rect.collidepoint(mouse_pos):
            main.running = False
            
    def move_collide_title(self, main, mouse_pos):
        if(self.single_game_rect.collidepoint(mouse_pos)):
            self.select_state = 0
        elif(self.option_rect.collidepoint(mouse_pos)):
            self.select_state = 1
        elif (self.exit_rect.collidepoint(mouse_pos)):
            self.select_state = 2
        
        self.apply_state_change()    
            
    def keydown_title(self, main, key):
        if key == self.user_data.key_left:
            self.select_state -= 1
            while(self.select_state < 0):
                self.select_state += STATE_NUMBER
        elif key == self.user_data.key_right:
            self.select_state += 1
            while(self.select_state >= STATE_NUMBER):
                self.select_state -= STATE_NUMBER
        elif key == self.user_data.key_enter:
            self.enter_state(main)
            return
        elif key == pygame.K_ESCAPE:
            self.on_option = True
        else:
            # 사용 가능한 키 보여주기
            return
        
        self.apply_state_change()
            
    def apply_state_change(self):
        screen_size = self.user_data.get_screen_size()
        self.button_select_pos = self.tup_mul(screen_size, self.button_select_default_poses[self.select_state])
        self.button_select_rect = self.button_select_img.get_rect(center = self.button_select_pos)
    
    def enter_state(self, main):
        if(self.select_state == STATE_SINGLE_GAME):
            main.scene_change(main.get_scene_index("single game"))
        elif(self.select_state == STATE_OPTION):
            self.on_option = True
        elif(self.select_state == STATE_EXIT):
            main.running = False
    
    def set_title_gui(self, screen_size):
        self.set_gui_pos(screen_size)
        self.set_gui_imges(screen_size)
        self.set_gui_rct()
        
    def change_screen_size(self):
        screen_size = self.user_data.get_screen_size()
        self.set_gui_imges(screen_size)
        self.set_gui_rct()
        
    def set_gui_default_pos(self):
        self.single_game_default_pos = (0.2, 0.7)
        self.option_default_pos = (0.6, 0.7)
        self.exit_default_pos = (0.8, 0.7)
        self.button_select_default_poses = [ (0.2, 0.65), (0.6, 0.65), (0.8, 0.65) ]
        
    def set_gui_pos(self, screen_size):
        self.single_game_pos = self.tup_mul(screen_size, self.single_game_default_pos)
        self.option_pos = self.tup_mul(screen_size, self.option_default_pos)
        self.exit_pos = self.tup_mul(screen_size, self.exit_default_pos)
        self.button_select_pos = self.tup_mul(screen_size, self.button_select_default_poses[self.select_state])
        
    def set_gui_imges(self, screen_size):
        scale_ratio = self.tup_div(screen_size, self.design_size)
        self.title_BG           = pygame.transform.scale(self.default_title_BG, scale_ratio)
        self.single_game_img    = pygame.transform.scale(self.default_single_game_img, scale_ratio)
        self.option_img         = pygame.transform.scale(self.default_option_img, scale_ratio)
        self.exit_img           = pygame.transform.scale(self.default_exit_img, scale_ratio)
        self.button_select_img  = pygame.transform.scale(self.default_button_select_img, scale_ratio)
        
    def set_gui_rct(self):
        self.single_game_rect = self.single_game_img.get_rect(center = self.single_game_pos)
        self.option_rect = self.option_img.get_rect(center = self.option_pos)
        self.exit_rect = self.exit_img.get_rect(center = self.exit_pos)
        self.button_select_rect = self.button_select_img.get_rect(center = self.button_select_pos)
        
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])
    
    def tup_div(self, tup1, tup2):
        return (tup1[0] / tup2[0], tup1[1] / tup2[1])
    
    