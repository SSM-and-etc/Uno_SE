import os

import pygame

from Lobby.lobby import Lobby
from GameData.user_data import UserData
from GameData.game_data import GameData
from Title.title import Title
from GamePlay.game_play import GamePlay
from StoryMode.storymode import StoryMode
from Sound.sound import Sound


class GameMain():
    def __init__(self):
        current_path = os.path.dirname(__file__) 
        self.root_path = os.path.join(current_path, os.pardir)
        
        self.running = True
        self.player_info=[]
        self.playerAI_number=0
        self.add_info
        self.scene_state = self.get_scene_index("title") # title: 0, single play: 1, ...
        self.game_data = GameData()
        self.user_data = UserData()
        self.sound = Sound(self)
        self.title = None
        self.play_game = None
        self.lobby = None
        self.stage_index = 1
        
        
        self.set_scene_obj(self.scene_state)
        self.set_screen()
        
        self.card_group       = pygame.sprite.Group()
        
        self.clock = pygame.time.Clock()
        
    def get_scene_index(self, scene_name):
        match scene_name:
            case "title":
                return 0
            case "single game":
                return 1
            case "game start":
                return 2
            case "story mode":
                return 3
            case "story mode game start":
                return 4
        return -1
        
    def get_scene_obj(self, scene_state):
        match scene_state:
            case 0:
                return self.title
            case 1:
                return self.lobby
            case 2:
                return self.play_game
            case 3:
                return self.storymode
            case 4:
                return self.play_game_storymode
            case _:
                return None

    def set_scene_obj(self, scene_state):
        match scene_state:
            case 0:
                self.title = Title(self)
            case 1:
                # 인자) 일반 모드: 0, 대전 상대 수 n / 스토리: 스테이지 n 을 인자로 추가
                self.player_info=[]
                self.lobby = Lobby(self)
            case 2:
                self.play_game = GamePlay(self,playerlist=self.player_info,stage_index=0,playerAI_number=self.playerAI_number)
            case 3:
                self.storymode = StoryMode(self)
            case 4:
                self.play_game_storymode = GamePlay(self, None, self.stage_index)
            case _:
                pass
    def reset_scene_obj(self, scene_state):
        match scene_state:
            case 0:
                self.title = None
            case 1:
                self.lobby = None
            case 2:
                self.play_game = None
            case 3:
                self.storymode = None
            case 4:
                self.play_game_storymode = None
            case _:
                pass
            
        
    def scene_change(self, next_scene_state):
        self.reset_scene_obj(self.scene_state)
        self.set_scene_obj(next_scene_state)
        self.sound.change_bgm(next_scene_state)
        
        self.scene_state = next_scene_state
        
        
    def set_screen(self):
        self.screen = pygame.display.set_mode(self.user_data.get_screen_size())
        
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
            
    def add_info(self,info):
        if info:
            for player in info:
                if player.clicked ==True:
                    self.playerAI_number+=1
                    self.player_info.append(player)
if __name__ == "__main__":
    # pygame.mixer.pre_init(44100,-16,2,512)
    pygame.init()
    pygame.display.set_caption("Uno game")
    gameMain = GameMain()
    gameMain.play()
    pygame.quit()