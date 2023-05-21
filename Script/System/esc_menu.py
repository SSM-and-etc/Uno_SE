import pygame

import os

from System.images import Images
from System.statebuttons import StateButtons
from System.texts import Texts
from System.achievements import Achievements
from System.option import Option


class EscMenu():
    def __init__(self, main, parent):
        self.main = main
        self.user_data = main.user_data
        self.option = Option(main, parent)
        self.achievements = Achievements(main)
        self.imgs = Images(main.user_data, main.root_path)
        self.buttons = StateButtons(main.user_data, main.root_path)
        
        self.add_assets()
        
        self.on_option = False
        self.on_achievements = False
        
    def display(self, main):
        self.draw(main.screen)
        self.on_esc = True
        if self.on_option:
            self.on_option = self.option.display(main)
        elif self.on_achievements:
            self.on_achievements = self.achievements.display(main)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main.running = False
                    
                if event.type == pygame.KEYDOWN:
                    self.keydown(main, event.key)
                
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.click_collide(main, event.pos)
                    
                if event.type == pygame.MOUSEMOTION:
                    self.move_collide(main, event.pos)
            
        return self.on_esc
    
    def draw(self, screen):
        self.imgs.draw(screen)
        self.buttons.draw(screen)
        
    def keydown(self, main, key):
        if not self.buttons.key_down_state(key):
            match key:
                case self.user_data.key_enter:
                    self.enter_state()
                case pygame.K_ESCAPE:
                    self.exit()
            
    def click_collide(self, main, mouse_pos):
        clicked_button_idx = self.buttons.get_clicked_button_idx(mouse_pos)
        if clicked_button_idx:
            self.enter_state()
        
    def move_collide(self, main, mouse_pos):
        self.buttons.get_clicked_button_idx(mouse_pos)
        
    def enter_state(self):
        match self.buttons.get_state()[0]:
            case 0:
                self.exit()
            case 1:
                self.on_option = True
            case 2:
                self.diplay_achievements()
            case 3:
                self.main.scene_change(self.main.get_scene_index("title"))
            case 4:
                self.main.running = False
        
    def diplay_achievements(self):
        self.on_achievements = True
        self.achievements.apply_check()
        
    
    def add_assets(self):
        self.add_imgs()
        self.add_buttons()
        self.add_texts()
        
    def add_imgs(self):
        self.imgs.add_row("Material/BG/esc.png", "Material/BG/esc.png", (0.5, 0.5))
        
    def add_buttons(self):
        self.buttons.add_row("Material/Button/Esc/continue.png", "Material/ColorMode/Esc/continue.png")
        self.buttons.add_row("Material/Button/Esc/option.png", "Material/ColorMode/Esc/option.png")
        self.buttons.add_row("Material/Button/Esc/achievements.png", "Material/ColorMode/Esc/achievements.png")
        self.buttons.add_row("Material/Button/Esc/main_menu.png", "Material/ColorMode/Esc/main_menu.png")
        self.buttons.add_row("Material/Button/Esc/exit.png", "Material/ColorMode/Esc/exit.png")
        for i in range(len(self.buttons.imgs)):
            self.buttons.set_row_linspace(i, 0, 1)
        self.buttons.set_col_linspace(0, 0.1, 0.9)
        
    def add_texts(self):
        pass
        
    def apply_screen_size(self):
        self.imgs.apply_screen_size()
        self.buttons.apply_screen_size()
        self.option.apply_screen_size()
        self.achievements.apply_screen_size()
        
    def exit(self):
        self.on_esc = False
        
        