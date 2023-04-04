import pygame

import os

class Option():
    def __init__(self, root, screen_size):
        self.option_BG = pygame.image.load(os.path.join(root, "Material/BG/title.png"))
        
    
    def display(self, main):
        pass