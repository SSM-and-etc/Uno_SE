import pygame

import os

from System.option import Option
from System.images import Images
from System.statebuttons import StateButtons
from System.texts import Texts

# Constants
STATE_NUMBER = 4
STATE_SINGLE_GAME = 0
STATE_STORY_MODE = 1
STATE_OPTION = 2
STATE_EXIT = 3
BLUE_MAGENTA = (153, 102, 204)

class Title():
    def __init__(self, main):
        self.main = main
        self.design_size = (1280, 720)
        self.user_data = main.user_data
        self.imgs = Images(main.user_data, main.root_path)
        self.buttons = StateButtons(main.user_data, main.root_path)
        self.ex_texts = Texts(main.user_data)
        
        self.add_assets()
        self.default_font_size = 30
        
        self.on_option = False
        self.select_state = 0 # 0: single game start, 1: option, 2: exit ...
        
        self.option = Option(main, self)
        
        self.set_title_gui(self.user_data.get_screen_size())
        self.ex_key_counter = 0
        
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
                    
                if event.type == pygame.USEREVENT and self.ex_key_counter > 0:
                    self.ex_key_counter -= 1
                    
            self.draw_title(main.screen)
            
    def draw_title(self, screen):
        self.imgs.draw(screen)
        self.buttons.draw(screen)
        if self.ex_key_counter > 0:
            self.ex_texts.draw(screen)
        
    def click_collide_title(self, main, mouse_pos):
        clicked_button_idx = self.buttons.get_clicked_button_idx(mouse_pos)
        if clicked_button_idx != None:
            self.enter_state(main, self.buttons.get_state()[1])
            
    def move_collide_title(self, main, mouse_pos):
        clicked_button_idx = self.buttons.get_clicked_button_idx(mouse_pos)
        if clicked_button_idx != None:
            pass
            
    def keydown_title(self, main, key):
        if self.buttons.key_down_state(key):
            pass
        elif key == self.user_data.key_enter:
            self.enter_state(main, self.buttons.get_state()[1])
        elif key == pygame.K_ESCAPE:
            self.on_option = True
        else:
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            self.ex_key_counter = 3
        
    
    def enter_state(self, main, state_i):
        match state_i:
            case 0:
                main.scene_change(main.get_scene_index("single game"))
            case 1:
                main.scene_change(main.get_scene_index("story mode"))
            case 2:
                main.scene_change(main.get_scene_index("multi game"))
            case 3:
                self.on_option = True
            case 4:
                pass # 업적 확인 연결
            case 5:
                main.running = False
    
    def set_title_gui(self, screen_size):
        self.set_text(screen_size)
        
    def change_screen_size(self):
        screen_size = self.user_data.get_screen_size()
        self.imgs.apply_screen_size()
        self.buttons.apply_screen_size()
        self.set_text(screen_size)
        
    def set_text(self, screen_size):
        self.ex_texts.change_text(0, self.get_ex_text())
        
    def add_assets(self):
        self.add_imgs()
        self.add_buttons()
        self.add_texts()
    
    def add_imgs(self):
        self.imgs.add_row("Material/BG/title.png", "Material/ColorMode/BG/title.png", (0.5, 0.5))
        
    def add_buttons(self):
        self.buttons.add_row("Material/Button/single_game.png", "Material/Button/single_game.png", (0, 0.7))
        self.buttons.add("Material/Button/story_mode.png", "Material/Button/story_mode.png", (0, 0.7))
        self.buttons.add("Material/Button/multi_game.png", "Material/Button/multi_game.png", (0, 0.7))
        self.buttons.add("Material/Button/option.png", "Material/Button/option.png", (0, 0.7))
        self.buttons.add("Material/Button/achievements.png", "Material/Button/achievements.png", (0, 0.7))
        self.buttons.add("Material/Button/exit.png", "Material/Button/exit.png", (0, 0.7))
        self.buttons.set_row_linspace(0, 0, 1)
        
    def add_texts(self):
        self.ex_texts.add(self.get_ex_text(), (0.27, 0.5))
        
    def get_ex_text(self):
        return "Left: " + pygame.key.name(self.user_data.key_left) + " , Right: " + pygame.key.name(self.user_data.key_right) + ", Enter: " + pygame.key.name(self.user_data.key_enter) + ", Esc: esc"