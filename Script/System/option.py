import pygame

import os
import copy

class Option():
    def __init__(self, root, user_data):
        self.temp_data = copy.copy(user_data)
        self.user_data = user_data
        
        self.load_asset(root)
        self.set_default_pos()
        
        self.select_state = [0, 0]
        self.cursor_state = [0, 0]
        self.on_select = False
        self.reset_on_option_state()
        self.set_option_gui()
        
    
    def display(self, main):
        self.on_option = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False
                
            if event.type == pygame.KEYDOWN:
                self.keydown_option(event.key)
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                self.click_collide_option(main, event.pos)
                
            if event.type == pygame.MOUSEMOTION:
                self.move_collide_option(event.pos)
            
        self.draw_option(main.screen)
        
        return self.on_option
            
    def draw_option(self, screen):
        screen.blit(self.pop_up_img, self.pop_up_rect)
        # 아래에서 위 순서로 그리기, 현재 선택지 표시는 제일 아래로
        self.draw_setting_buttons(screen)
        self.draw_volume_option(screen)
        self.draw_color_blindness_option(screen)
        self.draw_key_setting_option(screen)
        self.draw_screen_size_option(screen)
        self.draw_cursor(screen)
        self.draw_select(screen)
        
            
    def draw_screen_size_option(self, screen):
        screen.blit(self.screen_size_changer_button_img, self.screen_size_changer_button_rect)
        if(self.on_screen_changer):
            for i in range(len(self.screen_size_block_imges)):
                screen.blit(self.screen_size_block_imges[i], self.screen_size_block_rects[i])
        
    def draw_key_setting_option(self, screen):
        screen.blit(self.key_button_img, self.left_key_button_rect)
        screen.blit(self.key_button_img, self.right_key_button_rect)
        screen.blit(self.key_button_img, self.enter_key_button_rect)
        screen.blit(self.key_button_img, self.up_key_button_rect)
        screen.blit(self.key_button_img, self.down_key_button_rect)
        
    def draw_color_blindness_option(self, screen):
        if self.on_color_blindness_mode:
            screen.blit(self.checked_button_img, self.on_color_blindness_mode_rect)
        else:
            screen.blit(self.key_button_img, self.on_color_blindness_mode_rect)
        
    def draw_volume_option(self, screen):
        for i in range(len(self.volume_rects)):
            screen.blit(self.volume_img, self.volume_rects[i])
            screen.blit(self.sound_bar_img, self.sound_bar_rects[i])
        if self.temp_data.master_volume_off:
            screen.blit(self.volume_x_img, self.volume_x_poses[0])
        else:
            pass
        if self.temp_data.bgm_volume_off:
            screen.blit(self.volume_x_img, self.volume_x_poses[1])
        else:
            pass
        if self.temp_data.eft_volume_off:
            screen.blit(self.volume_x_img, self.volume_x_poses[2])
        else:
            pass
        # TODO: pass 자리에 현재 바 상태만큼 색칠
        
    def draw_setting_buttons(self, screen):
        screen.blit(self.save_img, self.save_rect)
        screen.blit(self.reset_img, self.reset_rect)
        screen.blit(self.exit_img, self.exit_rect)
        
    def draw_cursor(self, screen):
        if self.on_select:
            return
        screen.blit(self.button_cursor_img, self.button_cursor_rects[self.cursor_state[0]][self.cursor_state[1]])
    
    def draw_select(self, screen):
        if self.on_select:
            screen.blit(self.button_select_img, self.button_select_rects[self.select_state[0]][self.select_state[1]])
    
        
    def click_collide_option(self, main, mouse_pos):
        if self.on_screen_changer:
            self.click_collide_screen_size_option(main, mouse_pos)
            self.reset_on_option_state()
        elif self.click_collide_key_setting_option(mouse_pos) and self.on_key_setting:
            self.reset_on_option_state()
        elif self.screen_size_changer_button_rect.collidepoint(mouse_pos):
            self.on_screen_changer = not self.on_screen_changer
        elif not self.pop_up_rect.collidepoint(mouse_pos):
            self.on_option = False
        else:
            self.click_collide_color_blindness_option(mouse_pos)
    
    def click_collide_screen_size_option(self, main, mouse_pos):
        if self.on_screen_changer:
            for idx, rect in enumerate(self.screen_size_block_rects):
                if rect.collidepoint(mouse_pos):
                    self.change_screen_size(main, idx)
            
    def click_collide_key_setting_option(self, mouse_pos):
        if self.left_key_button_rect.collidepoint(mouse_pos):
            self.select_state = 0
        elif self.right_key_button_rect.collidepoint(mouse_pos):
            self.select_state = 1
        elif self.enter_key_button_rect.collidepoint(mouse_pos):
            self.select_state = 2
        elif self.up_key_button_rect.collidepoint(mouse_pos):
            self.select_state = 3
        elif self.down_key_button_rect.collidepoint(mouse_pos):
            self.select_state = 4    
        else:
            return True
        
        self.on_key_setting = True
        self.apply_key_state_change()
        return False
    
    def click_collide_color_blindness_option(self, mouse_pos):
        if self.on_color_blindness_mode_rect.collidepoint(mouse_pos):
            self.temp_data.color_blindness_mode = self.on_color_blindness_mode = not self.on_color_blindness_mode
            
    def move_collide_option(self, mouse_pos):
        if self.on_select:
            return
        self.move_collide_screen_size_option(mouse_pos)
        self.move_collide_key_setting_option(mouse_pos)
        self.move_collide_color_blindness_option(mouse_pos)
        self.move_collide_volume_option(mouse_pos)
        self.move_collide_setting_buttons(mouse_pos)
            
    def move_collide_screen_size_option(self, mouse_pos):
        if self.screen_size_changer_button_rect.collidepoint(mouse_pos):
            self.cursor_state = [0, 0]
            
    def move_collide_key_setting_option(self, mouse_pos):
        if self.left_key_button_rect.collidepoint(mouse_pos):
            self.cursor_state = [1, 0]
        elif self.right_key_button_rect.collidepoint(mouse_pos):
            self.cursor_state = [1, 1]
        elif self.enter_key_button_rect.collidepoint(mouse_pos):
            self.cursor_state = [1, 2]
        elif self.up_key_button_rect.collidepoint(mouse_pos):
            self.cursor_state = [2, 0]
        elif self.down_key_button_rect.collidepoint(mouse_pos):
            self.cursor_state = [2, 1]
            
    def move_collide_color_blindness_option(self, mouse_pos):
        if self.on_color_blindness_mode_rect.collidepoint(mouse_pos):
            self.cursor_state = [3, 0]
            
    def move_collide_volume_option(self, mouse_pos):
        for i in range(len(self.volume_rects)):
            if self.volume_rects[i].collidepoint(mouse_pos):
                self.cursor_state = [i + 4, 0]
                return
        for i in range(len(self.sound_bar_rects)):
            if self.sound_bar_rects[i].collidepoint(mouse_pos):
                self.cursor_state = [i + 4, 1]
            
    def move_collide_setting_buttons(self, mouse_pos):
        if self.save_rect.collidepoint(mouse_pos):
            self.cursor_state = [7, 0]
        elif self.reset_rect.collidepoint(mouse_pos):
            self.cursor_state = [7, 1]
        elif self.exit_rect.collidepoint(mouse_pos):
            self.cursor_state = [7, 2]
            
    def keydown_option(self, key):
        if(key == pygame.K_ESCAPE):
            self.on_option = False
        elif self.on_key_setting:
            self.change_key(key)
    
    def change_screen_size(self, main, screen_size_index):
        self.temp_data.set_screen_size(main, screen_size_index)
        self.screen_size_changer_button_img = self.screen_size_block_imges[self.temp_data.screen_size_index]
        
    def change_key(self, new_key):
        match self.select_state:
            case 0:
                self.temp_data.key_left = new_key
            case 1:
                self.temp_data.key_right = new_key
            case 2:
                self.temp_data.key_enter = new_key
                
    def apply_key_state_change(self):
        screen_size = self.temp_data.get_screen_size()
        self.button_select_pos = self.tup_mul(screen_size, self.button_select_default_poses[self.select_state])
        self.button_select_rect = self.button_select_img.get_rect(center = self.button_select_pos)
        
    def reset_on_option_state(self):
        self.on_key_setting = False
        self.on_screen_changer = False
        self.on_color_blindness_mode = False
        self.on_master_volume_mode = [False, False]
        self.on_bgm_volume_mode = [False, False]
        self.on_eft_volume_mode = [False, False]
        
    def reset_option(self):
        self.reset_on_option_state()
        self.temp_data.reset_data()
        
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])
    
    def save_data(self):
        self.user_data = copy.copy(self.temp_data)
        
    def load_asset(self, root):
        self.pop_up_img = pygame.image.load(os.path.join(root, "Material/GUI/option_pop_up.png"))
        self.screen_size_block_imges = \
            [
                pygame.image.load(os.path.join(root, "Material/button/640_480.png")),
                pygame.image.load(os.path.join(root, "Material/button/1280_720.png")),
                pygame.image.load(os.path.join(root, "Material/button/1920_1080.png")),
                pygame.image.load(os.path.join(root, "Material/button/2560_1440.png"))
            ]
        self.key_button_img = pygame.image.load(os.path.join(root, "Material/button/key_button.png"))
        self.checked_button_img = pygame.image.load(os.path.join(root, "Material/button/checked_button.png"))
        self.volume_img  = pygame.image.load(os.path.join(root, "Material/Option/volume.png"))
        self.volume_x_img  = pygame.image.load(os.path.join(root, "Material/Option/volume_x.png"))
        self.sound_bar_img = pygame.image.load(os.path.join(root, "Material/Option/sound_bar.png"))
        self.save_img = pygame.image.load(os.path.join(root, "Material/Option/save.png"))
        self.reset_img = pygame.image.load(os.path.join(root, "Material/Option/reset.png"))
        self.exit_img = pygame.image.load(os.path.join(root, "Material/Option/exit.png"))
        
        self.button_select_img = pygame.image.load(os.path.join(root, "Material/Button/button_select.png"))
        self.button_cursor_img = pygame.image.load(os.path.join(root, "Material/Button/button_cursor.png"))
    
    def set_default_pos(self):
        self.pop_up_default_pos = (0.5, 0.5)
        self.screen_size_changer_button_default_pos = (0.6, 0.15)
        self.screen_size_block_default_poses = \
            [
                (0.6, 0.2), 
                (0.6, 0.25), 
                (0.6, 0.3), 
                (0.6, 0.35)
            ]
        self.left_key_button_default_pos = (0.535, 0.225)
        self.right_key_button_default_pos = (0.625, 0.225)
        self.enter_key_button_default_pos = (0.715, 0.225)
        self.up_key_button_default_pos = (0.535, 0.315)
        self.down_key_button_default_pos = (0.625, 0.315)
        self.on_color_blindness_mode_default_pos = (0.535, 0.395)
        self.volume_default_poses = \
            [
                (0.49, 0.485),
                (0.49, 0.575),
                (0.49, 0.665)
            ]
        self.volume_x_default_poses = \
            [
                (0.51, 0.485),
                (0.51, 0.575),
                (0.51, 0.665)
            ]
        self.sound_bar_default_poses = \
            [
                (0.62, 0.485),
                (0.62, 0.575),
                (0.62, 0.665)
            ]
        self.save_default_pos = (0.35, 0.85)
        self.reset_default_pos = (0.5, 0.85)
        self.exit_default_pos = (0.65, 0.85)
        
        self.button_select_default_poses = \
            [
                [(0.6, 0.1), (0.6, 0.15), (0.6, 0.2), (0.6, 0.25), (0.6, 0.3)],
                [(0.535, 0.175), (0.625, 0.175), (0.715, 0.175)],
                [(0.535, 0.265), (0.625, 0.265)],
                [(0.535, 0.345)],
                [(0.49, 0.44), (0.62, 0.44)],
                [(0.49, 0.53), (0.62, 0.53)],
                [(0.49, 0.62), (0.62, 0.62)],
                [(0.35, 0.78), (0.5, 0.78), (0.65, 0.78)]
            ]
            
    def set_option_gui(self):
        screen_size = self.temp_data.get_screen_size()
        self.screen_size_changer_button_img = self.screen_size_block_imges[self.temp_data.screen_size_index]
        
        self.pop_up_pos = self.tup_mul(screen_size, self.pop_up_default_pos)
        self.screen_size_block_poses = [self.tup_mul(screen_size, pos) for pos in self.screen_size_block_default_poses]
        self.screen_size_changer_button_pos = self.tup_mul(screen_size, self.screen_size_changer_button_default_pos)
        self.left_key_button_pos = self.tup_mul(screen_size, self.left_key_button_default_pos)
        self.right_key_button_pos = self.tup_mul(screen_size, self.right_key_button_default_pos)
        self.enter_key_button_pos = self.tup_mul(screen_size, self.enter_key_button_default_pos)
        self.up_key_button_pos = self.tup_mul(screen_size, self.up_key_button_default_pos)
        self.down_key_button_pos = self.tup_mul(screen_size, self.down_key_button_default_pos)
        self.on_color_blindness_mode_pos = self.tup_mul(screen_size, self.on_color_blindness_mode_default_pos)
        self.volume_poses = [self.tup_mul(screen_size, pos) for pos in self.volume_default_poses]
        self.volume_x_poses = [self.tup_mul(screen_size, pos) for pos in self.volume_x_default_poses]
        self.sound_bar_poses = [self.tup_mul(screen_size, pos) for pos in self.sound_bar_default_poses]
        self.save_pos = self.tup_mul(screen_size, self.save_default_pos)
        self.reset_pos = self.tup_mul(screen_size, self.reset_default_pos)
        self.exit_pos = self.tup_mul(screen_size, self.exit_default_pos)
        
        self.button_select_poses = [[self.tup_mul(screen_size, pos) for pos in poses] for poses in self.button_select_default_poses]
        self.button_cursor_poses = self.button_select_poses
        
        self.pop_up_rect = self.pop_up_img.get_rect(center = self.pop_up_pos)
        self.screen_size_block_rects = [self.screen_size_block_imges[i].get_rect(center = self.screen_size_block_poses[i]) for i in range(len(self.screen_size_block_imges))]
        self.screen_size_changer_button_rect = self.screen_size_changer_button_img.get_rect(center = self.screen_size_changer_button_pos)
        self.left_key_button_rect = self.key_button_img.get_rect(center = self.left_key_button_pos)
        self.right_key_button_rect = self.key_button_img.get_rect(center = self.right_key_button_pos)
        self.enter_key_button_rect = self.key_button_img.get_rect(center = self.enter_key_button_pos)
        self.up_key_button_rect = self.key_button_img.get_rect(center = self.up_key_button_pos)
        self.down_key_button_rect = self.key_button_img.get_rect(center = self.down_key_button_pos)
        self.on_color_blindness_mode_rect = self.key_button_img.get_rect(center = self.on_color_blindness_mode_pos)
        self.volume_rects = [self.volume_img.get_rect(center = pos) for pos in self.volume_poses]
        self.volume_x_rects = [self.volume_x_img.get_rect(center = pos) for pos in self.volume_x_poses]
        self.sound_bar_rects = [self.sound_bar_img.get_rect(center = pos) for pos in self.sound_bar_poses]
        self.save_rect = self.save_img.get_rect(center = self.save_pos)
        self.reset_rect = self.reset_img.get_rect(center = self.reset_pos)
        self.exit_rect = self.exit_img.get_rect(center = self.exit_pos)
        
        self.button_select_rects = [[self.button_select_img.get_rect(center = pos) for pos in poses] for poses in self.button_select_poses]
        self.button_cursor_rects = [[self.button_cursor_img.get_rect(center = pos) for pos in poses] for poses in self.button_cursor_poses]