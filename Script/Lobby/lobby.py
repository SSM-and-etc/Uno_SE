import pygame

from Lobby.input_box import InputBox
from Lobby.button import StartButton
class Lobby():
    def __init__(self,main):
        self.WHITE = (255, 255, 255)
        self.ORANGE= (255, 163, 0)
        self.font= pygame.font.Font(None, 36)
        self.lobby_img = pygame.image.load("Material/BG/Title.png")
        self.ratio_list=[(0.8,0.05),(0.8,0.2),(0.8,0.35),(0.8,0.5),(0.8,0.65),(0.8,0.8)]
        self.player_box_info=[]
        self.player_list=[]
        self.screen= main.screen
        self.screen_width=main.screen.get_width()
        self.screen_heigth=main.screen.get_height()
        self.make_screen(self.screen_width,self.screen_heigth, self.ratio_list)
        self.mouse_pos=pygame.mouse.get_pos()
        self.start_button=StartButton("Start", self.screen_width*0.4, self.screen_heigth*0.6, self.screen_width/6, self.screen_heigth/10,self.ORANGE,self.font, self.screen,self.play_game)
        self.play_game
        self.main=main
        for i,info in enumerate(self.player_box_info):
            self.player_list.append(InputBox(info[0],info[1],info[2],info[3],i,'player'+str(i)))
    def display(self,main):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start_button.handle_event(event)
            for computer in self.player_list:
                computer.handle_event(event)
                            
        main.screen.blit(self.lobby_img, (0, 0))
        for computer in self.player_list:
            computer.draw(main.screen)
        self.start_button.draw()
            
    def make_screen(self,width,height,ratios):
        for ratio in ratios:
            self.player_box_info.append((width*ratio[0], height*ratio[1],self.screen_width/6,self.screen_heigth/12))
    def play_game(self):
       self.main.add_info(self.player_list)
       self.main.scene_change(self.main.get_scene_index("game start"))