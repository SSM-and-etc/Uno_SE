# 배경 이미지 설정
import os

import pygame

from GameData.UserData import UserData


# 현재 파일의 위치 반환
current_path = os.path.dirname(__file__) 
root_path = os.path.join(current_path, os.pardir)
print(root_path)

# 배경 이미지 불러오기(임시, 다른 클래스로 옮기는 것이 좋을지?)
background      = pygame.image.load(os.path.join(root_path, "Material/BG/Title.png"))

class GameMain():
    def __init__(self):
        self.card_group       = pygame.sprite.Group()
        
        self.running = True
        
        self.user_data = UserData()
        
        self.screen = pygame.display.set_mode((self.user_data.screen_width, self.user_data.screen_height))
        self.state = 0 # 0: Title, 1: play(single)
        self.clock = clock = pygame.time.Clock()
        
        
        
    def group_reset(self):
        self.card_group.empty()
        
    def play_title(self):
        self.screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                pass
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pass
                
        # self.class.update(self)
        self.card_group.update(self)

        # self.class.draw(screen)
        
    def play_single_game(self):
        pass
                

    def play(self):
        self.clock.tick(30)
        while self.running:
            
            if self.state == 0:
                self.play_title()
            elif self.state == 1:
                self.play_single_game()
                
            
            pygame.display.update()
            
    


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Uno game")
    gameMain = GameMain()
    gameMain.play()
    pygame.quit()