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
        self.default_checked_imgs = []
        self.default_checked_imgs_c = []
        self.default_poses = []
        self.imgs = []
        self.imgs_c = []
        self.checked_imgs = []
        self.checked_imgs_c = []
        self.rects = []
        self.is_checked = []
        
    def draw(self, screen):
        if self.user_data.color_blindness_mode:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    if self.is_checked[i][j]:
                        screen.blit(self.checked_imgs_c[i][j], self.rects[i][j])
                    else:
                        screen.blit(self.imgs_c[i][j], self.rects[i][j])
        else:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    if self.is_checked[i][j]:
                        screen.blit(self.checked_imgs[i][j], self.rects[i][j])
                    else:
                        screen.blit(self.imgs[i][j], self.rects[i][j])
             
    def add_row(self, img_path, img_path_c = None, pos = (0, 0), checked_img_path = None, checked_img_path_c = None):
        self.default_imgs.append([])
        self.default_imgs_c.append([])
        self.default_checked_imgs.append([])
        self.default_checked_imgs_c.append([])
        self.default_poses.append([])
        self.imgs.append([])
        self.imgs_c.append([])
        self.rects.append([])
        self.checked_imgs.append([])
        self.checked_imgs_c.append([])
        self.is_checked.append([])
        self.add(img_path, img_path_c, pos, checked_img_path, checked_img_path_c)
             
    def add(self, img_path, img_path_c = None, pos = (0, 0), checked_img_path = None, checked_img_path_c = None):
        if not img_path_c:
            img_path_c = img_path
        if not checked_img_path:
            checked_img_path = img_path
        if not checked_img_path_c:
            checked_img_path_c = img_path_c
        self.default_imgs[-1].append(pygame.image.load(os.path.join(self.root, img_path)))
        self.default_imgs_c[-1].append(pygame.image.load(os.path.join(self.root, img_path_c)))
        self.default_checked_imgs[-1].append(pygame.image.load(os.path.join(self.root, checked_img_path)))
        self.default_checked_imgs_c[-1].append(pygame.image.load(os.path.join(self.root, checked_img_path_c)))
        self.default_poses[-1].append(pos)
        self.imgs[-1].append(None)
        self.imgs_c[-1].append(None)
        self.rects[-1].append(None)
        self.checked_imgs[-1].append(None)
        self.checked_imgs_c[-1].append(None)
        self.is_checked[-1].append(False)
        
        i, j = len(self.imgs) - 1, len(self.imgs[-1]) - 1
        self.apply_img_scale(self.get_scale_ratio(), i, j)
        self.apply_rect_scale(i, j)
        
    def set_checked(self, i, j, is_checked):
        self.is_checked[i][j] = is_checked
        
    def get_checked(self, i, j):
        return self.is_checked[i][j]
        
    def set_row_linspace(self, i, start, end):
        linspace = np.linspace(start, end, len(self.imgs[i]) + 2)[1:-1]
        for j in range(len(self.imgs[i])):
            self.default_poses[i][j] = (linspace[j], self.default_poses[i][j][1])
            self.apply_rect_scale(i, j)
        
    def set_col_linspace(self, j, start, end):
        linspace = np.linspace(start, end, len(self.imgs) + 2)[1:-1]
        for i in range(len(self.imgs)):
            self.default_poses[i][j] = (self.default_poses[i][j][0], linspace[i])
            self.apply_rect_scale(i, j)
        
    def get_img(self, i, j):
        return self.default_imgs[i][j], self.default_imgs_c[i][j], self.default_checked_imgs[i][j], self.default_checked_imgs_c[i][j]
        
    def change_img(self, i, j, imgs):
        self.default_imgs[i][j] = imgs[0]
        self.default_imgs_c[i][j] = imgs[1]
        self.default_checked_imgs[i][j] = imgs[2]
        self.default_checked_imgs_c[i][j] = imgs[3]
        self.apply_img_scale(self.get_scale_ratio(), i, j)
        self.apply_rect_scale(i, j)
        
    def apply_img_scale(self, scale_ratio, i, j):
        self.imgs[i][j] = pygame.transform.scale(self.default_imgs[i][j], self.tup_mul(self.get_img_size(self.default_imgs[i][j]), scale_ratio))
        self.imgs_c[i][j] = pygame.transform.scale(self.default_imgs_c[i][j], self.tup_mul(self.get_img_size(self.default_imgs_c[i][j]), scale_ratio))
        self.checked_imgs[i][j] = pygame.transform.scale(self.default_checked_imgs[i][j], self.tup_mul(self.get_img_size(self.default_checked_imgs[i][j]), scale_ratio))
        self.checked_imgs_c[i][j] = pygame.transform.scale(self.default_checked_imgs_c[i][j], self.tup_mul(self.get_img_size(self.default_checked_imgs_c[i][j]), scale_ratio))
        
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