import pygame

import os
from Lobby.input_box import InputBox

class Lobby:
    def __init__(self,screen_size):
        self.lobby_img = pygame.image.load( "Material/BG/Title.png")
        # self.single_game_default_pos = (0.2, 0.7)
        # self.story_mode_default_pos = (0.4, 0.7)
        # self.option_default_pos = (0.6, 0.7)
        # self.exit_default_pos = (0.8, 0.7)
        
        self.on_title_gui = True
        self.mouse_pos=pygame.mouse.get_pos()    
        # self.apply_state_change()
        self.player= InputBox(0, 50, 200, 32, 0, 'player')
        self.computer1= InputBox(50, 50, 200, 32, 1, 'computer1')
        self.computer2= InputBox(50, 100, 200, 32, 2, 'computer2')
        self.computer3= InputBox(50, 150, 200, 32, 3, 'computer3')
        self.computer4= InputBox(50, 200, 200, 32, 4, 'computer4') 
        self.computer5= InputBox(50, 250, 200, 32, 5, 'computer5')
        self.player=[self.computer1,self.computer2,self.computer3,self.computer4,self.computer5]
        # self.screen= pygame.display.set_mode((640, 480))
        # self.draw_lobby
        
    def display(self,main):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # main.running = False
                 pygame.quit()
                 exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            for computer in self.player:
                computer.handle_event(event)
       
            #     if self.rect.collidepoint(event.pos):
            #         self.active = not self.active
            #     else:
            #         self.active = False
            # if event.type == pygame.KEYDOWN:
            #     if self.active:
            #         if event.key == pygame.K_RETURN:
            #             # Enter 키를 누르면 Input Box의 텍스트를 출력합니다.
            #             self.active=False
            #             # self.text_dic[self.key] = self.text
            #         elif event.key == pygame.K_BACKSPACE:
            #             # 백스페이스 키를 누르면 Input Box의 텍스트에서 마지막 문자를 삭제합니다.
            #             # self.text_dic[self.key] = self.text[:-1]
            #             self.text = self.text[:-1]
            #         else:
            #             # 키 입력이 있으면 Input Box의 텍스트에 추가합니다.
            #             # self.text_dic[self.key] +=event.unicode
            #             self.text += event.unicode
                            
        main.screen.blit(self.lobby_img, (0, 0))
        for computer in self.player:
            computer.draw(main.screen)
        # if(self.on_title_gui):
        #     
            
    # def draw_lobby(self,screen):
       
        # pygame.draw.rect(screen, self.color, self.input_box, 2)
        # text_surface = self.font.render(self.text, True, (0, 0, 0))
        # screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        # screen.blit(self.lobby_img)
        # pygame.display.flip()  
    # def collide_title(self, main, mouse_pos):
    #     if(self.single_game_rect.collidepoint(mouse_pos)):
    #         # TODO: 싱글 게임 시작 호출
    #         pass
    #     elif(self.story_mode_rect.collidepoint(mouse_pos)):
    #         self.on_title_gui = False
    #         # TODO: 옵션창 호출
    #     elif(self.option_rect.collidepoint(mouse_pos)):
    #         self.on_title_gui = False
    #         # TODO: 옵션창 호출
    #     elif (self.self.exit_rect.collidepoint(mouse_pos)):
    #         main.running = False
            
    # def keydown_title(self, main, key):
    #     if(key == main.user_data.key_left):
    #         self.select_state -= 1
    #         while(self.select_state < 0):
    #             self.select_state += STATE_NUMBER
    #     elif(key == main.user_data.key_right):
    #         self.select_state += 1
    #         while(self.select_state >= STATE_NUMBER):
    #             self.select_state -= STATE_NUMBER
    #     elif(key == main.user_data.key_enter):
    #         self.enter_state(main)
    #         return
    #     else:
    #         # 사용 가능한 키 보여주기
    #         return
        
    #     self.apply_state_change()
            
    # def apply_state_change(self):
    #     # TODO: 현재 state에 따라 select 이미지 적절하게 이동시키기
    #     pass
    
    # def enter_state(self, main):
    #     if(self.select_state == STATE_SINGLE_GAME):
    #         # TODO: 싱글 게임 시작 호출 
    #         pass
    #     elif(self.select_state == STATE_STORY_MODE):
    #         self.on_title_gui = False
    #         # TODO: 스토리 모드 호출 
    #         pass
    #     elif(self.select_state == STATE_OPTION):
    #         self.on_title_gui = False
    #         # TODO: 옵션창 호출
    #         pass
    #     elif(self.select_state == STATE_EXIT):
    #         main.running = False
        
    
    # def set_lobby_gui(self, screen_size):
        # self.single_game_pos = self.tup_mul(screen_size, self.single_game_default_pos)
        # self.story_mode_pos = self.tup_mul(screen_size, self.story_mode_default_pos)
        # self.option_pos = self.tup_mul(screen_size, self.option_default_pos)
        # self.exit_pos = self.tup_mul(screen_size, self.exit_default_pos)
        
        # self.single_game_rect = self.single_game_img.get_rect(center = self.single_game_pos)
        # self.story_mode_rect = self.story_mode_img.get_rect(center = self.story_mode_pos)
        # self.option_rect = self.option_img.get_rect(center = self.option_pos)
        # self.exit_rect = self.exit_img.get_rect(center = self.exit_pos)
        
    # def tup_mul(self, tup1, tup2):
    #     return (tup1[0] * tup2[0], tup1[1] * tup2[1])   