import pygame

import os
import copy

from GameData.user_data import UserData

ORANGE = (255, 153, 51)

class Option():
    def __init__(self, main, parent):
        self.parent = parent
        self.main = main
        self.design_size = (1280, 720)
        self.user_data = main.user_data
        self.temp_data = UserData()
        self.temp_data.copy_data(self.user_data)
        
        self.load_asset(main.root_path)
        self.set_gui_default_poses()
        self.default_font_size = 17
        
        self.set_option_gui()
        self.reset_on_option_state()
        self.set_key_hold_down()
        
    
    def display(self, main):
        self.on_option = True
        
        self.move_collide_option(self.last_mouse_pos)
        if self.on_key_hold and self.on_select:
            self.keyhold_option()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False
            if event.type == pygame.KEYDOWN:
                self.key_down_hold_check(event.key)
                self.keydown_option(main, event.key)
            
            if event.type == pygame.KEYUP:
                self.key_up_hold_check(event.key)
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                self.click_collide_option(main, event.pos)
                #pygame.MOUSEBUTTONUP
                
            if event.type == pygame.MOUSEMOTION:
                self.last_mouse_pos = event.pos
            
        self.draw_option(main.screen)
        
        return self.on_option
    
    def exit_option(self):
        self.on_option = False
        self.temp_data.copy_data(self.user_data)
        self.reset_on_option_state()
        self.set_option_gui()
            
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
        if(self.on_select and self.select_state[0] == 0):
            for i in range(len(self.screen_size_block_imges)):
                screen.blit(self.screen_size_block_imges[i], self.screen_size_block_rects[i])
        
    def draw_key_setting_option(self, screen):
        screen.blit(self.key_button_img, self.left_key_button_rect)
        screen.blit(self.key_button_img, self.right_key_button_rect)
        screen.blit(self.key_button_img, self.enter_key_button_rect)
        screen.blit(self.key_button_img, self.up_key_button_rect)
        screen.blit(self.key_button_img, self.down_key_button_rect)
        
        screen.blit(self.left_key_text, self.left_key_text_pos)
        screen.blit(self.right_key_text, self.right_key_text_pos)
        screen.blit(self.enter_key_text, self.enter_key_text_pos)
        screen.blit(self.up_key_text, self.up_key_text_pos)
        screen.blit(self.down_key_text, self.down_key_text_pos)
        
    def draw_color_blindness_option(self, screen):
        if self.temp_data.color_blindness_mode:
            screen.blit(self.checked_button_img, self.on_color_blindness_mode_rect)
        else:
            screen.blit(self.key_button_img, self.on_color_blindness_mode_rect)
        
    def draw_volume_option(self, screen):
        for i in range(len(self.volume_rects)):
            if self.temp_data.volumes_off[i]:
                screen.blit(self.volume_x_img, self.volume_x_poses[i])
            else: # 색칠 한 후에 sound_bar가 그려져야 사각형 외각이 가려지므로 주의
                pygame.draw.rect(screen, ORANGE, self.fill_sound_bar_rects[i])
            screen.blit(self.volume_img, self.volume_rects[i])
            screen.blit(self.sound_bar_img, self.sound_bar_rects[i])
        
    def draw_setting_buttons(self, screen):
        screen.blit(self.save_img, self.save_rect)
        screen.blit(self.reset_img, self.reset_rect)
        screen.blit(self.exit_img, self.exit_rect)
        screen.blit(self.game_exit_img, self.game_exit_rect)
        
        if self.user_data.color_blindness_mode:
            screen.blit(self.reset_CM_img, self.reset_rect)
        else:
            screen.blit(self.reset_img, self.reset_rect)
        
    def draw_cursor(self, screen):
        if self.on_select:
            return
        screen.blit(self.button_cursor_img, self.button_cursor_rects[self.cursor_state[0]][self.cursor_state[1]])
    
    def draw_select(self, screen):
        if self.on_select:
            if self.user_data.color_blindness_mode:
                screen.blit(self.button_select_CM_img, self.button_select_rects[self.select_state[0]][self.select_state[1]])
            else:
                screen.blit(self.button_select_img, self.button_select_rects[self.select_state[0]][self.select_state[1]])
    
        
    def click_collide_option(self, main, mouse_pos):
        # TODO: on_select 상태에 따라 클릭을 이분 하는 방식으로 리펙토링
        if not self.pop_up_rect.collidepoint(mouse_pos):
            if self.on_select:
                self.on_select = False
            else:
                self.exit_option()
        elif self.click_collide_screen_size_option(main, mouse_pos):
            return
        elif self.click_collide_key_setting_option(mouse_pos):
            return
        elif self.click_collide_color_blindness_option(mouse_pos):
            return
        elif self.click_collide_volume_option(mouse_pos):
            return
        elif self.click_collide_setting_buttons(mouse_pos):
            return
        else:
            self.on_select = False
    
    def click_collide_screen_size_option(self, main, mouse_pos):
        if self.screen_size_changer_button_rect.collidepoint(mouse_pos):
            if not self.on_select:
                self.select_state = self.cursor_state.copy()
        elif self.on_select and self.select_state[0] == 0:
            for idx, rect in enumerate(self.screen_size_block_rects):
                if rect.collidepoint(mouse_pos):
                    self.change_screen_size(main, idx)
        else:
            return False
        self.on_select = not self.on_select
        return True
            
    def click_collide_key_setting_option(self, mouse_pos):
        if self.left_key_button_rect.collidepoint(mouse_pos) or self.right_key_button_rect.collidepoint(mouse_pos) \
            or self.enter_key_button_rect.collidepoint(mouse_pos) or self.up_key_button_rect.collidepoint(mouse_pos) \
                or self.down_key_button_rect.collidepoint(mouse_pos):
            self.select_state = self.cursor_state.copy()
        elif self.on_select and (self.cursor_state[0] == 1 or self.cursor_state[0] == 2):
            pass
        else:
            return False
        self.on_select = not self.on_select
        return True
    
    def click_collide_color_blindness_option(self, mouse_pos):
        if self.on_color_blindness_mode_rect.collidepoint(mouse_pos):
            if self.on_select:
                self.on_select = False
            self.temp_data.color_blindness_mode = not self.temp_data.color_blindness_mode
        else:
            return False
        return True
    
    def click_collide_volume_option(self, mouse_pos):
        for i in range(len(self.temp_data.volumes)):
            if self.volume_rects[i].collidepoint(mouse_pos):
                if self.on_select:
                    self.on_select = False
                else:
                    self.temp_data.volumes_off[i] = not self.temp_data.volumes_off[i]
                return True
            if self.sound_bar_rects[i].collidepoint(mouse_pos):
                if self.on_select and not self.select_state[0] == i + 4:
                    self.on_select = False
                else:
                    self.select_state = self.cursor_state.copy()
                    self.on_select = True
                    self.change_fill_bar_pos(i, mouse_pos[0])
                return True
        return False
    
    def click_collide_setting_buttons(self, mouse_pos):
        if self.on_select:
            if self.save_rect.collidepoint(mouse_pos) or self.reset_rect.collidepoint(mouse_pos) or self.exit_rect.collidepoint(mouse_pos) or self.game_exit_rect.collidepoint(mouse_pos):
                self.on_select = False
            else:
                return False
        else:
            if self.save_rect.collidepoint(mouse_pos):
                self.save_data()
                self.exit_option()
            elif self.reset_rect.collidepoint(mouse_pos):
                self.reset_option()
            elif self.exit_rect.collidepoint(mouse_pos):
                self.exit_option()
            elif self.game_exit_rect.collidepoint(mouse_pos):
                self.main.scene_change(self.main.get_scene_index("title"))
                #self.exit_option()
            else:
                return False
        return True
        
    def move_collide_option(self, mouse_pos):
        self.move_collide_screen_size_option(mouse_pos)
        if self.on_select:
            return
        self.move_collide_key_setting_option(mouse_pos)
        self.move_collide_color_blindness_option(mouse_pos)
        self.move_collide_volume_option(mouse_pos)
        self.move_collide_setting_buttons(mouse_pos)
            
    def move_collide_screen_size_option(self, mouse_pos):
        if self.screen_size_changer_button_rect.collidepoint(mouse_pos):
            self.cursor_state = [0, 0]
        elif self.on_select and self.select_state[0] == 0:
            for i in range(len(self.screen_size_block_rects)):
                if self.screen_size_block_rects[i].collidepoint(mouse_pos):
                    self.select_state[1] = i + 1
                    return
            
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
        elif self.game_exit_rect.collidepoint(mouse_pos):
            self.cursor_state = [8, 0]
            
    def keyhold_option(self):
        if self.cursor_state[0] >= 4 and self.cursor_state[0] <= 6:
            if self.left_hold:
                self.sound_bars_w[self.cursor_state[0] - 4] -= 1
            elif self.right_hold:
                self.sound_bars_w[self.cursor_state[0] - 4] += 1
            else:
                return
            self.change_fill_bar_width(self.cursor_state[0] - 4, self.sound_bars_w[self.cursor_state[0] - 4])
            
    def keydown_option(self, main, key):
        # 해상도 입력 상태, 키 입력 상태, 사운드 입력 상태 총 세가지 경우 예외 처리 후 방향키 이동
        if key == pygame.K_ESCAPE:
            if self.on_select:
                self.on_select = False
            else:
                self.exit_option()
        elif self.on_select:
            self.key_down_on_select_state(main, key)
        else:
            self.key_down_on_cursur_state(main, key)

    def key_down_on_select_state(self, main, key):
        if self.cursor_state[0] == 0: # 해상도 부분
            if key == self.user_data.key_up:
                self.select_state[1] -= 1
                self.screen_size_option_index_handling()
            elif key == self.user_data.key_down:
                self.select_state[1] += 1
                self.screen_size_option_index_handling()
            elif self.select_state[1] != 0 and key == self.user_data.key_enter:
                self.change_screen_size(main, self.select_state[1] - 1)
                self.on_select = False
        elif self.cursor_state[0] == 1 or self.cursor_state[0] == 2: # 키 입력 부분
            self.change_key(key)
            self.on_select = False
        elif self.cursor_state[0] >= 4 and self.cursor_state[0] <= 6: # 사운드 바
            if key == self.user_data.key_left:
                self.sound_bars_w[self.cursor_state[0] - 4] -= 1
            elif key == self.user_data.key_right:
                self.sound_bars_w[self.cursor_state[0] - 4] += 1
            elif key == self.user_data.key_enter:
                self.on_select = False
            else:
                return
            self.change_fill_bar_width(self.cursor_state[0] - 4, self.sound_bars_w[self.cursor_state[0] - 4])
            
    def key_down_on_cursur_state(self, main, key):
        if key == self.user_data.key_left:
            self.cursor_state[1] -= 1
        elif key == self.user_data.key_right:
            self.cursor_state[1] += 1
        elif key == self.user_data.key_up:
            self.cursor_state[0] -= 1
            if self.cursor_state[1] >= len(self.button_cursor_poses[self.cursor_state[0]]):
                self.cursor_state[1] = len(self.button_cursor_poses[self.cursor_state[0]]) - 1
        elif key == self.user_data.key_down:
            self.cursor_state[0] += 1
            if self.cursor_state[0] >= len(self.button_cursor_poses):
                self.cursor_state[0] -= len(self.button_cursor_poses)
            if self.cursor_state[1] >= len(self.button_cursor_poses[self.cursor_state[0]]):
                self.cursor_state[1] = len(self.button_cursor_poses[self.cursor_state[0]]) - 1
        elif key == self.user_data.key_enter:
            self.enter_state()
            return
        else:
            return
        self.option_cursor_index_handling()
            
    def screen_size_option_index_handling(self):
        if self.select_state[1] < 1:
            self.select_state[1] += 4
        elif self.select_state[1] > 4:
            self.select_state[1] -= 4
    
    def option_cursor_index_handling(self):
        if self.cursor_state[0] == 0:
            self.cursor_state[1] = 0 # 해상도 커서는 0에만(첫 상자에) 고정되게
        elif self.cursor_state[0] < 0:
            self.cursor_state[0] += len(self.button_cursor_poses)
        elif self.cursor_state[0] >= len(self.button_cursor_poses):
            self.cursor_state[0] -= len(self.button_cursor_poses)
        elif self.cursor_state[1] < 0:
            self.cursor_state[1] += len(self.button_cursor_poses[self.cursor_state[0]])
        elif self.cursor_state[1] >= len(self.button_cursor_poses[self.cursor_state[0]]):
            self.cursor_state[1] -= len(self.button_cursor_poses[self.cursor_state[0]])
        
    def enter_state(self):
        if self.cursor_state[0] == 3:
            self.temp_data.color_blindness_mode = not self.temp_data.color_blindness_mode
        elif self.cursor_state[0] >= 4 and self.cursor_state[0] <= 6:
            if self.cursor_state[1] == 0:
                self.temp_data.volumes_off[self.cursor_state[0] - 4] = not self.temp_data.volumes_off[self.cursor_state[0] - 4]
            elif self.cursor_state[1] == 1:
                self.select_state = self.cursor_state.copy()
                self.on_select = True
        elif self.cursor_state[0] == 7:
            match self.cursor_state[1]:
                case 0:
                    self.save_data()
                    self.exit_option()
                case 1:
                    self.reset_option()
                case 2:
                    self.exit_option()
        else:
            self.select_state = self.cursor_state.copy()
            self.on_select = True
    
    def change_screen_size(self, main, screen_size_index):
        self.temp_data.set_screen_size(main, screen_size_index)
        self.screen_size_changer_button_img = self.screen_size_block_imges[self.temp_data.screen_size_index]
        
    def change_key(self, new_key):
        match self.select_state[0]:
            case 1:
                self.temp_data.set_key(self.select_state[1], new_key)
            case 2:    
                self.temp_data.set_key(self.select_state[1] + 3, new_key)
        self.set_text(self.user_data.get_screen_size())
                
    def apply_key_state_change(self):
        screen_size = self.temp_data.get_screen_size()
        self.button_select_pos = self.tup_mul(screen_size, self.button_select_default_poses[self.select_state])
        self.button_select_rect = self.button_select_img.get_rect(center = self.button_select_pos)
        
    def key_down_hold_check(self, key):
        if key == self.user_data.key_left:
            self.left_hold = True
        elif key == self.user_data.key_right:
            self.right_hold = True
        if self.is_key_holding():
            self.on_key_hold = True    
        
    def key_up_hold_check(self, key):
        if key == self.user_data.key_left:
            self.left_hold = False
        elif key == self.user_data.key_right:
            self.right_hold = False
        if not self.is_key_holding():
            self.on_key_hold = False
            
    def is_key_holding(self):
        if self.left_hold or self.right_hold:
            return True
        else:
            return False
        
    def change_fill_bar_pos(self, bar_idx, xpos_right):
        xpos_right = min(self.fill_sound_bar_xposes_max[bar_idx], xpos_right)
        xpos_right = max(self.fill_sound_bar_xposes_min[bar_idx], xpos_right)
        w = xpos_right - self.fill_sound_bar_xposes_min[bar_idx]
        self.fill_sound_bar_rects[bar_idx][2] = w
        self.temp_data.volumes[bar_idx] = w / self.sound_bar_rects[bar_idx].width
        self.temp_data.volumes_off[bar_idx] = False
        
    def change_fill_bar_width(self, bar_idx, width):
        self.sound_bars_w[bar_idx] = max(0, self.sound_bars_w[bar_idx])
        self.sound_bars_w[bar_idx] = min(self.sound_bar_rects[0].width, self.sound_bars_w[bar_idx])
        self.fill_sound_bar_rects[bar_idx][2] = self.sound_bars_w[bar_idx]
        self.temp_data.volumes[bar_idx] = self.sound_bars_w[bar_idx] / self.sound_bar_rects[bar_idx].width
        self.temp_data.volumes_off[bar_idx] = False   
        if self.sound_bars_w[bar_idx] == 0:
            self.temp_data.volumes_off[bar_idx] = True
        
    def reset_on_option_state(self):
        self.select_state = [0, 0]
        self.cursor_state = [0, 0]
        self.on_select = False
        self.last_mouse_pos = (0, 0)
        self.set_drawing_options()
        
    def reset_option(self):
        self.temp_data.reset_data()
        self.reset_on_option_state()
        
    def save_data(self):
        self.user_data.copy_data(self.temp_data)
        self.user_data.save_data(self.main)
        self.set_option_gui()
        self.parent.change_screen_size()
        self.main.sound.set_volume()
        
    def load_asset(self, root):
        self.default_pop_up_img                 = pygame.image.load(os.path.join(root, "Material/GUI/option_pop_up.png"))
        self.default_screen_size_block_imges    = \
        [
            pygame.image.load(os.path.join(root, "Material/button/640_480.png")),
            pygame.image.load(os.path.join(root, "Material/button/1280_720.png")),
            pygame.image.load(os.path.join(root, "Material/button/1920_1080.png")),
            pygame.image.load(os.path.join(root, "Material/button/2560_1440.png"))
        ]
        self.default_key_button_img             = pygame.image.load(os.path.join(root, "Material/button/key_button.png"))
        self.default_checked_button_img         = pygame.image.load(os.path.join(root, "Material/button/checked_button.png"))
        self.default_volume_img                 = pygame.image.load(os.path.join(root, "Material/Option/volume.png"))
        self.default_volume_x_img               = pygame.image.load(os.path.join(root, "Material/Option/volume_x.png"))
        self.default_sound_bar_img              = pygame.image.load(os.path.join(root, "Material/Option/sound_bar.png"))
        self.default_save_img                   = pygame.image.load(os.path.join(root, "Material/Option/save.png"))
        self.default_reset_img                  = pygame.image.load(os.path.join(root, "Material/Option/reset.png"))
        self.default_reset_CM_img               = pygame.image.load(os.path.join(root, "Material/ColorMode/colormode_reset.png"))
        self.default_exit_img                   = pygame.image.load(os.path.join(root, "Material/Option/exit.png"))
        self.default_game_exit_img              = pygame.image.load(os.path.join(root, "Material/Button/exit.png"))
        self.default_button_select_img          = pygame.image.load(os.path.join(root, "Material/Button/button_select.png"))
        self.default_button_cursor_img          = pygame.image.load(os.path.join(root, "Material/Button/button_cursor.png"))
        self.default_button_select_CM_img       = pygame.image.load(os.path.join(root, "Material/ColorMode/colormode_button_select.png"))
    
    def set_gui_default_poses(self):
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
            (0.505, 0.475),
            (0.505, 0.565),
            (0.505, 0.655)
        ]
        self.sound_bar_default_poses = \
        [
            (0.62, 0.485),
            (0.62, 0.575),
            (0.62, 0.665)
        ]
        self.save_default_pos = (0.35, 0.77)
        self.reset_default_pos = (0.5, 0.77)
        self.exit_default_pos = (0.65, 0.77)
        self.game_exit_default_pos = (0.65, 0.85)
        
        self.button_select_default_poses = \
        [
            [(0.6, 0.1), (0.6, 0.15), (0.6, 0.2), (0.6, 0.25), (0.6, 0.3)],
            [(0.535, 0.175), (0.625, 0.175), (0.715, 0.175)],
            [(0.535, 0.265), (0.625, 0.265)],
            [(0.535, 0.345)],
            [(0.49, 0.44), (0.62, 0.44)],
            [(0.49, 0.53), (0.62, 0.53)],
            [(0.49, 0.62), (0.62, 0.62)],
            [(0.35, 0.70), (0.5, 0.70), (0.65, 0.70)],
            [(0.65, 0.80)],
        ]
        
        self.left_key_text_default_pos = (0.52, 0.21)
        self.right_key_text_default_pos = (0.61, 0.21)
        self.enter_key_text_default_pos = (0.7, 0.21)
        self.up_key_text_default_pos = (0.52, 0.30)
        self.down_key_text_default_pos = (0.61, 0.300)
        
    def set_gui_poses(self, screen_size):
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
        self.game_exit_pos = self.tup_mul(screen_size, self.game_exit_default_pos)
        
        self.button_select_poses = [[self.tup_mul(screen_size, pos) for pos in poses] for poses in self.button_select_default_poses]
        self.button_cursor_poses = self.button_select_poses
        
        self.left_key_text_pos  = self.tup_mul(screen_size, self.left_key_text_default_pos )
        self.right_key_text_pos = self.tup_mul(screen_size, self.right_key_text_default_pos )
        self.enter_key_text_pos = self.tup_mul(screen_size, self.enter_key_text_default_pos )
        self.up_key_text_pos    = self.tup_mul(screen_size, self.up_key_text_default_pos )
        self.down_key_text_pos  = self.tup_mul(screen_size, self.down_key_text_default_pos)
            
    def set_gui_imges(self, screen_size):
        scale_ratio = self.tup_div(screen_size, self.design_size)
        self.pop_up_img                 = pygame.transform.scale(self.default_pop_up_img              , self.tup_mul(self.get_img_size(self.default_pop_up_img),scale_ratio))
        self.screen_size_block_imges    = [pygame.transform.scale(img , self.tup_mul(self.get_img_size(img),scale_ratio)) for img in self.default_screen_size_block_imges]
        self.key_button_img             = pygame.transform.scale(self.default_key_button_img          , self.tup_mul(self.get_img_size(self.default_key_button_img),scale_ratio))
        self.checked_button_img         = pygame.transform.scale(self.default_checked_button_img      , self.tup_mul(self.get_img_size(self.default_checked_button_img),scale_ratio))
        self.volume_img                 = pygame.transform.scale(self.default_volume_img              , self.tup_mul(self.get_img_size(self.default_volume_img),scale_ratio))
        self.volume_x_img               = pygame.transform.scale(self.default_volume_x_img            , self.tup_mul(self.get_img_size(self.default_volume_x_img),scale_ratio))
        self.sound_bar_img              = pygame.transform.scale(self.default_sound_bar_img           , self.tup_mul(self.get_img_size(self.default_sound_bar_img),scale_ratio))
        self.save_img                   = pygame.transform.scale(self.default_save_img                , self.tup_mul(self.get_img_size(self.default_save_img),scale_ratio))
        self.reset_img                  = pygame.transform.scale(self.default_reset_img               , self.tup_mul(self.get_img_size(self.default_reset_img),scale_ratio))
        self.reset_CM_img               = pygame.transform.scale(self.default_reset_CM_img            , self.tup_mul(self.get_img_size(self.default_reset_img),scale_ratio))
        self.exit_img                   = pygame.transform.scale(self.default_exit_img                , self.tup_mul(self.get_img_size(self.default_exit_img),scale_ratio))
        self.game_exit_img              = pygame.transform.scale(self.default_game_exit_img           , self.tup_mul(self.get_img_size(self.default_game_exit_img),scale_ratio))
        self.button_select_img          = pygame.transform.scale(self.default_button_select_img       , self.tup_mul(self.get_img_size(self.default_button_select_img ),scale_ratio))
        self.button_cursor_img          = pygame.transform.scale(self.default_button_cursor_img       , self.tup_mul(self.get_img_size(self.default_button_cursor_img),scale_ratio))
        self.button_select_CM_img       = pygame.transform.scale(self.default_button_select_CM_img    , self.tup_mul(self.get_img_size(self.default_button_select_img ),scale_ratio))
        self.screen_size_changer_button_img = self.screen_size_block_imges[self.user_data.screen_size_index].copy()   
            
            
    def set_gui_rct(self):
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
        self.game_exit_rect = self.game_exit_img.get_rect(center = self.game_exit_pos)
        self.button_select_rects = [[self.button_select_img.get_rect(center = pos) for pos in poses] for poses in self.button_select_poses]
        self.button_cursor_rects = [[self.button_cursor_img.get_rect(center = pos) for pos in poses] for poses in self.button_cursor_poses]
            
    def set_text(self, screen_size):
        font_ratio = (screen_size[0]/self.design_size[0] + screen_size[1]/self.design_size[1]) / 2
        font = pygame.font.SysFont("arial", int(self.default_font_size * font_ratio), True, True)
        
        self.left_key_text   = font.render(pygame.key.name(self.temp_data.key_left), True, ORANGE)
        self.right_key_text  = font.render(pygame.key.name(self.temp_data.key_right), True, ORANGE)
        self.enter_key_text  = font.render(pygame.key.name(self.temp_data.key_enter), True, ORANGE)
        self.up_key_text     = font.render(pygame.key.name(self.temp_data.key_up), True, ORANGE)
        self.down_key_text   = font.render(pygame.key.name(self.temp_data.key_down), True, ORANGE)
            
    def set_option_gui(self):
        screen_size = self.user_data.get_screen_size() 
        self.set_gui_poses(screen_size)
        self.set_gui_imges(screen_size)
        self.set_gui_rct()
        self.set_text(screen_size)
        
    def set_drawing_options(self):
        self.screen_size_changer_button_img = self.screen_size_block_imges[self.user_data.screen_size_index]
        self.fill_sound_bar_xposes_max = [rect.right for rect in self.sound_bar_rects]
        self.fill_sound_bar_xposes_min = [rect.left for rect in self.sound_bar_rects]
        w = self.sound_bar_rects[0].width
        self.fill_sound_bar_rects = [[self.sound_bar_rects[i].left, self.sound_bar_rects[i].top, w * self.user_data.volumes[i], self.sound_bar_rects[i].height] for i in range(len(self.sound_bar_rects))] # x, y, w, h
        self.sound_bars_w = [w * volume for volume in self.user_data.volumes]
    
    def set_key_hold_down(self):
        self.on_key_hold = False
        self.left_hold = False
        self.right_hold = False
        #self.up_hold = False
        #self.down_hold = False
        #self.enter_hold = False        
        
    def get_img_size(self, img):
        return (img.get_width(), img.get_height())    
        
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])
    
    def tup_div(self, tup1, tup2):
        return (tup1[0] / tup2[0], tup1[1] / tup2[1])