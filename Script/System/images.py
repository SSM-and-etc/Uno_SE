import pygame
import numpy as np

import os

class Images():
    def __init__(self, data, root, design_size = (1280, 720)):
        self.user_data = data
        self.root = root
        self.design_size = design_size
        self.default_imgs = []
        self.default_imgs_c = []
        self.default_poses = []
        self.imgs = []
        self.imgs_c = []
        self.rects = []
        
    def draw(self, screen):
        if self.user_data.color_blindness_mode:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    screen.blit(self.imgs_c[i][j], self.rects[i][j])
        else:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    screen.blit(self.imgs[i][j], self.rects[i][j])
             
    def add_row(self, img_path, img_path_c, pos, select_state_delta_pos = (0, -0.05)):
        self.default_imgs.append([])
        self.default_imgs_c.append([])
        self.default_poses.append([])
        self.imgs.append([])
        self.imgs_c.append([])
        self.rects.append([])
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
        
        i, j = len(self.imgs) - 1, len(self.imgs[-1]) - 1
        self.apply_img_scale(self.get_scale_ratio(), i, j)
        self.apply_rect_scale(i, j)
        
    def set_row_linspace(self, i, start, end):
        linspace = np.linspace(start, end, len(self.imgs[i] + 2))[1:-1]
        for j in range(len(self.imgs[i])):
            self.default_poses[i][j] = (linspace[i], self.default_poses[i][j][1])
            self.apply_rect_scale(i, j)
        
    def set_col_linspace(self, j, start, end):
        linspace = np.linspace(start, end, len(self.imgs + 2))[1:-1]
        for i in range(len(self.imgs)):
            self.default_poses[i][j] = (self.default_poses[i][j][0], linspace[i])
            self.apply_rect_scale(i, j)
        
    def change_img(self, img, i, j):
        self.default_imgs[i][j] = img
        self.apply_img_scale(self.get_scale_ratio(), i, j)
        self.apply_rect_scale(i, j)
        
    def apply_img_scale(self, scale_ratio, i, j):
        self.imgs[i][j] = pygame.transform.scale(self.default_imgs[i][j], self.tup_mul(self.get_img_size(self.default_imgs[i][j]), scale_ratio))
        self.imgs_c[i][j] = pygame.transform.scale(self.default_imgs_c[i][j], self.tup_mul(self.get_img_size(self.default_imgs[i][j]), scale_ratio))
        
    def apply_rect_scale(self, i, j):
        self.rects[i][j] = self.imgs[i][j].get_rect(center = self.get_scaled_pos(self.default_poses[i][j]))
        
    def apply_screen_size(self):
        scale_ratio = self.get_scale_ratio()
        for i in range(len(self.imgs)):
            for j in range(len(self.imgs[i])):
                self.apply_img_scale(scale_ratio, i, j)
                self.apply_rect_scale(i, j)
            
    def get_scaled_pos(self, default_pos):
        return self.tup_mul(self.user_data.get_screen_size(), default_pos)
                
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])
    
    def tup_div(self, tup1, tup2):
        return (tup1[0] / tup2[0], tup1[1] / tup2[1])
    
    def get_img_size(self, img):
        return (img.get_width(), img.get_height())
    
    def get_scale_ratio(self):
        return self.tup_div(self.user_data.get_screen_size(), self.design_size)