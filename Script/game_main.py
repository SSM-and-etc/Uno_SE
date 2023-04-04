import os

import pygame

from GameData.user_data import UserData
from GameData.game_data import GameData
from Title.title import Title


class GameMain():
    def __init__(self):
        current_path = os.path.dirname(__file__) 
        root_path = os.path.join(current_path, os.pardir)
        
        self.card_group       = pygame.sprite.Group()
        
        self.running = True
        
        self.game_data = GameData()
        self.user_data = UserData()
        self.title = Title(root_path, self.user_data.get_screen_size())
        
        self.set_screen(self.user_data.screen_width, self.user_data.screen_height)
        self.state = 0 # 0: Title, 1: play(single)
        self.clock = pygame.time.Clock()
        
    def set_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        
    def group_reset(self):
        self.card_group.empty()
        
        # self.class.update(self)
        self.card_group.update(self)

        # self.class.draw(screen)
        
    def play_single_game(self):
        pass
                

    def play(self):
        self.clock.tick(30)
        while self.running:
            
            if self.state == 0:
                self.title.display(self, self.screen)
            elif self.state == 1:
                self.play_single_game()
                
            
            pygame.display.update()
            
    


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Uno game")
    gameMain = GameMain()
    gameMain.play()
    pygame.quit()