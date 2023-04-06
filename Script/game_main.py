import os

import pygame

from GameData.user_data import UserData
from GameData.game_data import GameData
from Title.title import Title
from System.option import Option
from GamePlay.game_play import GamePlay


class GameMain():
    def __init__(self):
        current_path = os.path.dirname(__file__) 
        self.root_path = os.path.join(current_path, os.pardir)
        
        
        self.running = True
        
        self.scene_state = 0 # 0: Title, 1: play(single)
        self.game_data = GameData()
        self.user_data = UserData()
        self.title = None
        self.play_game = None
        self.option = None
        
        
        self.set_scene_obj(self.scene_state)
        self.set_screen(self.user_data.screen_width, self.user_data.screen_height)
        
        self.card_group       = pygame.sprite.Group()
        
        self.clock = pygame.time.Clock()
        
        
    def get_scene_obj(self, scene_state):
        match scene_state:
            case -1:
                return self.option
            case 0:
                return self.title
            case 1:
                return self.play_game
            case _:
                return None
            
    def set_scene_obj(self, scene_state):
        match scene_state:
            case -1:
                self.option = Option()
            case 0:
                self.title = Title(self.root_path, self.user_data.get_screen_size())
            case 1:
                self.play_game = GamePlay()
            case _:
                pass
                
    def reset_scene_obj(self, scene_state):
        match scene_state:
            case -1:
                self.option = None
            case 0:
                self.title = None
            case 1:
                self.play_game = None
            case _:
                pass
        
    def scene_change(self, next_scene_state):
        self.reset_scene_obj(self.scene_state)
        self.set_scene_obj(next_scene_state)
        
        self.scene_state = next_scene_state
        
        
    def set_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        
    def group_reset(self):
        self.card_group.empty()
        
        # self.class.update(self)
        self.card_group.update(self)

        # self.class.draw(screen)
        
    def play(self):
        self.clock.tick(30)
        while self.running:
            self.get_scene_obj(self.scene_state).display(self)
            pygame.display.update()
            

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Uno game")
    gameMain = GameMain()
    gameMain.play()
    pygame.quit()