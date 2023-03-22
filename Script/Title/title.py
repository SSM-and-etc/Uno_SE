import pygame

import os


class Title():
    def __init__(self, root, screen_size):
        self.title_BG = pygame.image.load(os.path.join(root, "Material/BG/title.png"))
        self.single_game_img = pygame.image.load(os.path.join(root, "Material/Button/single_game.png"))
        self.option_img = pygame.image.load(os.path.join(root, "Material/Button/option.png"))
        self.exit_img = pygame.image.load(os.path.join(root, "Material/Button/exit.png"))
        self.button_select_img = pygame.image.load(os.path.join(root, "Material/Button/button_select.png"))

        self.single_game_default_pos = (0.2, 0.7)
        self.option_default_pos = (0.6, 0.7)
        self.exit_default_pos = (0.8, 0.7)
        
        self.set_title_gui(screen_size)
        
    def display(self, main, screen):
        screen.blit(self.title_BG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False
                
            if event.type == pygame.KEYDOWN:
                pass
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pass
        
        self.draw_title(screen)
            
    def draw_title(self, screen):
        screen.blit(self.single_game_img, self.single_game_rect)
        screen.blit(self.option_img, self.option_rect)
        screen.blit(self.exit_img, self.exit_rect)
    
    def set_title_gui(self, screen_size):
        self.single_game_pos = self.tup_mul(screen_size, self.single_game_default_pos)
        self.option_pos = self.tup_mul(screen_size, self.option_default_pos)
        self.exit_pos = self.tup_mul(screen_size, self.exit_default_pos)
        
        self.single_game_rect = self.single_game_img.get_rect(center = self.single_game_pos)
        self.option_rect = self.option_img.get_rect(center = self.option_pos)
        self.exit_rect = self.exit_img.get_rect(center = self.exit_pos)
        
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])
    