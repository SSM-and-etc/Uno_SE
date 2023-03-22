import pygame

import os


class Title():
    def __init__(self, root):
        self.title_BG = pygame.image.load(os.path.join(root, "Material/BG/title.png"))
    
    def display(self, main, screen):
        screen.blit(self.title_BG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False
                
            if event.type == pygame.KEYDOWN:
                pass
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pass