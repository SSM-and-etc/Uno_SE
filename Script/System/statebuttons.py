import pygame

import os

from System.images import Images


class StateButtons(Images): 
    def __init__(self, data, root, design_size = (1280, 720)):
        super().__init__(data, root, design_size)
        self.state = [0, 0]
        self.is_state_holding = False
        self.on_state = True
        self.state_rects = []
        
        self.set_state_img()
        
    def draw(self, screen):
        if self.user_data.color_blindness_mode:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    screen.blit(self.imgs_c[i][j], self.rects[i][j])
            if self.on_state:
                if self.is_state_holding:
                    screen.blit(self.state_imgs_c[1], self.state_rects[self.state[0]][self.state[1]])
                else:
                    screen.blit(self.state_imgs_c[0], self.state_rects[self.state[0]][self.state[1]])
        else:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    screen.blit(self.imgs[i][j], self.rects[i][j])
            if self.on_state:
                if self.is_state_holding:
                    screen.blit(self.state_imgs[1], self.state_rects[self.state[0]][self.state[1]])
                else:
                    screen.blit(self.state_imgs[0], self.state_rects[self.state[0]][self.state[1]])
        
    def get_clicked_button_idx(self, mouse_pos):
        for i in range(len(self.imgs)):
            for j in range(len(self.imgs[i])):
                if self.rects[i][j].collidepoint(mouse_pos):
                    self.state = [i, j]
                    return i, j
        return None
    
    def key_down_state(self, key):
        match key:
            case self.user_data.key_left: 
                self.state[1] -= 1
            case self.user_data.key_right:
                self.state[1] += 1
            case self.user_data.key_up:
                self.state[0] -= 1
                if self.state[1] >= len(self.imgs[self.state[0]]):
                    self.state[1] = len(self.imgs[self.state[0]]) - 1
            case self.user_data.key_down:
                self.state[0] += 1
                if self.state[1] >= len(self.imgs[self.state[0]]):
                    self.state[1] = len(self.imgs[self.state[0]]) 
            case pygame.K_ESCAPE:
                if self.is_state_holding:
                    self.is_state_holding = False
                else:
                    return False
            case _:
                return False
        
        self.state_index_handling()
        return True
                
    def state_index_handling(self):
        if self.state[0] < 0:
            self.state[0] += len(self.imgs)
        elif self.state[0] >= len(self.imgs):
            self.state[0] -= len(self.imgs)
        elif self.state[1] < 0:
            self.state[1] += len(self.imgs[self.state[0]])
        elif self.state[1] >= len(self.imgs[self.state[0]]):
            self.state[1] -= len(self.imgs[self.state[0]])
        
    def add_row(self, img_path, img_path_c, pos):
        self.default_imgs.append([])
        self.default_imgs_c.append([])
        self.default_poses.append([])
        self.imgs.append([])
        self.imgs_c.append([])
        self.rects.append([])
        self.state_rects.append([])
        self.add(img_path, img_path_c, pos)
             
    def add(self, img_path, img_path_c, pos):
        img = pygame.image.load(os.path.join(self.root, img_path))
        img_c = pygame.image.load(os.path.join(self.root, img_path_c))
        self.default_imgs[-1].append(img)
        self.default_imgs_c[-1].append(img_c)
        self.default_poses[-1].append(pos)
        self.imgs[-1].append(None)
        self.imgs_c[-1].append(None)
        self.rects[-1].append(None)
        self.state_rects[-1].append(None)
        
        i, j = len(self.imgs) - 1, len(self.imgs[-1]) - 1
        self.apply_img_scale(self.get_scale_ratio(), i, j)
        self.apply_rect_scale(i, j)
        
    def apply_rect_scale(self, i, j):
        self.rects[i][j] = self.imgs[i][j].get_rect(center = self.get_scaled_pos(self.default_poses[i][j]))
        self.state_rects[i][j] = self.state_imgs[0].get_rect(midbottom = self.rects[i][j].midtop)
                
    def apply_screen_size(self):
        scale_ratio = self.get_scale_ratio()
        for i in range(len(self.imgs)):
            for j in range(len(self.imgs[i])):
                self.apply_img_scale(scale_ratio, i, j)
                self.apply_rect_scale(i, j)
        for i in range(len(self.default_state_imgs)):
            self.state_imgs[i] = pygame.transform.scale(self.default_state_imgs[i], self.tup_mul(self.get_img_size(self.default_state_imgs[i]), scale_ratio))
            self.state_imgs_c[i] = pygame.transform.scale(self.default_state_imgs_c[i], self.tup_mul(self.get_img_size(self.default_state_imgs_c[i]), scale_ratio))     
    
    def get_button_pos(self, i, j):
        return self.rects[i][j].center
    
    def set_state_img(self):
        self.default_state_imgs = []
        self.default_state_imgs.append(pygame.image.load(os.path.join(self.root, "Material/Button/button_cursor.png")))
        self.default_state_imgs.append(pygame.image.load(os.path.join(self.root, "Material/Button/button_select.png")))
        self.default_state_imgs_c = []
        self.default_state_imgs_c.append(pygame.image.load(os.path.join(self.root, "Material/Button/button_cursor.png")))
        self.default_state_imgs_c.append(pygame.image.load(os.path.join(self.root, "Material/ColorMode/colormode_button_select.png")))
        
        scale_ratio = self.get_scale_ratio()
        self.state_imgs = []
        self.state_imgs_c = []
        for i in range(len(self.default_state_imgs)):
            self.state_imgs.append(pygame.transform.scale(self.default_state_imgs[i], self.tup_mul(self.get_img_size(self.default_state_imgs[i]), scale_ratio)))
            self.state_imgs_c.append(pygame.transform.scale(self.default_state_imgs_c[i], self.tup_mul(self.get_img_size(self.default_state_imgs_c[i]), scale_ratio)))
    
    def get_state(self):
        return self.state[0], self.state[1]
    
    def set_state(self, is_on):
        self.on_state = is_on