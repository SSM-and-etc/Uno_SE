import pygame

import os

class Option():
    def __init__(self, root, user_data):
        self.pop_up_img = pygame.image.load(os.path.join(root, "Material/GUI/pop_up.png"))
        self.screen_size_block_imges = \
            [
                pygame.image.load(os.path.join(root, "Material/button/640_480.png")),
                pygame.image.load(os.path.join(root, "Material/button/1280_720.png")),
                pygame.image.load(os.path.join(root, "Material/button/1920_1080.png")),
                pygame.image.load(os.path.join(root, "Material/button/2560_1440.png"))
            ]
        
        self.pop_up_default_pos = (0.5, 0.5)
        self.screen_size_block_default_poses = \
            [
                (0.6, 0.35), 
                (0.6, 0.39), 
                (0.6, 0.43), 
                (0.6, 0.47)
            ]
        
        self.on_screen_changer = False
        self.on_key_setting = False
        self.user_data = user_data
        self.set_option_gui(self.user_data.get_screen_size())
    
    def display(self, main):
        on_option = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False
                
            if event.type == pygame.KEYDOWN:
                on_option = self.keydown_option(main, event.key)
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                self.click_collide_option(main, event.pos)
                
            if event.type == pygame.MOUSEMOTION:
                self.move_collide_option(main, event.pos)
            
        self.draw_option(main.screen)
        
        return on_option
            
    def draw_option(self, screen):
        screen.blit(self.pop_up_img, self.pop_up_rect)
        for i in range(len(self.screen_size_block_imges)):
            screen.blit(self.screen_size_block_imges[i], self.screen_size_block_rects[i])
        
    def click_collide_option(self, main, mouse_pos):
        pass
            
    def move_collide_option(self, main, mouse_pos):
        pass  
            
    def keydown_option(self, main, key):
        if(key == pygame.K_ESCAPE):
            return False
        
        return True
        
    
    def change_screen_size(self, screen_size_index):
        self.user_data.set_screen_size(screen_size_index)
        
    def change_key(self, key_idx, new_key):
        match key_idx:
            case 0:
                self.user_data.key_left = new_key
            case 1:
                self.user_data.key_right = new_key
            case 2:
                self.user_data.key_enter = new_key
                
    def set_option_gui(self, screen_size):
        self.pop_up_pos = self.tup_mul(screen_size, self.pop_up_default_pos)
        self.screen_size_block_poses = [self.tup_mul(screen_size, pos) for pos in self.screen_size_block_default_poses]
        
        self.pop_up_rect = self.pop_up_img.get_rect(center = self.pop_up_pos)
        self.screen_size_block_rects = [self.screen_size_block_imges[i].get_rect(center = self.screen_size_block_poses[i]) for i in range(len(self.screen_size_block_imges))]
        
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])