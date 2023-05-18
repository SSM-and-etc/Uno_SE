import pygame

import os

from images import Images


class StateButtons(Images): 
    def __init__(self, data, root, design_size = (1280, 720)):
        super.__init__(data, root, design_size)
        self.state = [0, 0]
        self.is_state_holding = False
        
        
    def draw(self, screen):
        if self.user_data.color_blindness_mode:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    screen.blit(self.imgs_c[i][j], self.rects[i][j])
        else:
            for i in range(len(self.imgs)):
                for j in range(len(self.imgs[i])):
                    screen.blit(self.imgs[i][j], self.rects[i][j])
                
        if self.is_state_holding:
            pass
        else:
            pass
                
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
    
    def get_button_pos(self, i, j):
        return self.rects[i][j].center
    
    def get_state(self):
        return self.state[0], self.state[1]