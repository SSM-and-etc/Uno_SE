import pygame

from System.option import Option
from System.images import Images
from System.statebuttons import StateButtons
from System.texts import Texts
from System.achievements import Achievements
from System.esc_menu import EscMenu

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
        self.user_data = main.user_data
        self.imgs = Images(main.user_data, main.root_path)
        self.buttons = StateButtons(main.user_data, main.root_path)
        self.ex_texts = Texts(main.user_data)
        
        self.add_assets()
        
        self.on_option = False
        self.on_achievements = False
        self.on_esc = False
        self.select_state = 0 # 0: single game start, 1: option, 2: exit ...
        
        self.option = Option(main, self)
        self.achievements = Achievements(main)
        self.esc = EscMenu(main, self)
        
        self.set_text(self.user_data.get_screen_size())
        self.ex_key_counter = 0
        
    def display(self, main):
        self.draw_title(main.screen)
        if self.on_option:
            self.on_option = self.option.display(main)
        elif self.on_achievements:
            self.on_achievements = self.achievements.display(main)
        elif self.on_esc:
            self.on_esc = self.esc.display(main)
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
            
    def draw_title(self, screen):
        self.imgs.draw(screen)
        self.buttons.draw(screen)
        if self.ex_key_counter > 0:
            self.ex_texts.draw(screen)
        
    def click_collide_title(self, main, mouse_pos):
        clicked_button_idx = self.buttons.get_clicked_button_idx(mouse_pos)
        if clicked_button_idx != None:
            self.enter_state(main)
            
    def move_collide_title(self, main, mouse_pos):
        clicked_button_idx = self.buttons.get_clicked_button_idx(mouse_pos)
        if clicked_button_idx != None:
            pass
            
    def keydown_title(self, main, key):
        if self.buttons.key_down_state(key):
            pass
        elif key == self.user_data.key_enter:
            self.enter_state(main)
        elif key == pygame.K_ESCAPE:
            self.on_esc = True
        else:
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            self.ex_key_counter = 3
        
    
    def enter_state(self, main):
        match self.buttons.get_state()[1]:
            case 0:
                main.scene_change(main.get_scene_index("single game"))
            case 1:
                main.scene_change(main.get_scene_index("story mode"))
            case 2:
                main.scene_change(main.get_scene_index("multi game"))
            case 3:
                self.on_option = True
            case 4:
                self.on_achievements = True
            case 5:
                main.running = False
    
        
    def change_screen_size(self):
        screen_size = self.user_data.get_screen_size()
        self.imgs.apply_screen_size()
        self.buttons.apply_screen_size()
        self.set_text(screen_size)
        self.option.apply_screen_size()
        self.achievements.apply_screen_size()
        self.esc.apply_screen_size()
        
    def set_text(self, screen_size):
        self.ex_texts.change_text(0, self.get_ex_text())
        
    def add_assets(self):
        self.add_imgs()
        self.add_buttons()
        self.add_texts()
        
    def apply_screen_size(self):
        self.imgs.apply_screen_size()
        self.buttons.apply_screen_size()
        self.ex_texts.apply_screen_size()
    
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