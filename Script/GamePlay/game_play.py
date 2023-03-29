import pygame

from uno.game import Game
from uno.player import Player
import random

import os


class Asset:
    def __init__(self, img_path, pos, mag=1.0):
        self.mag = (mag, mag)
        self.pos = pos

        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale_by(self.img, self.mag)

        self.rect = self.img.get_rect().move(pos)

    def set_image(self, img_path):
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale_by(self.img, self.mag)
        self.rect = self.img.get_rect().move(self.pos)


class GamePlay:
    def __init__(self, main):
        self.main = main

        design_resolution = (1280, 720)
        screen_size = main.user_data.get_screen_size()

        self.assets = {
            "background": Asset(os.path.join(main.root_path, "Material/BG/game.png"), (0, 0)),
            "deck": Asset(os.path.join(main.root_path, "Material/Card/deck.png"), (180, 150), mag=0.3),
            "button_uno": Asset(os.path.join(main.root_path, "Material/Button/button_uno.png"), (610, 300)),
            "table": Asset(os.path.join(main.root_path, "Material/Card/deck.png"), (360, 150), mag=0.3)
        }

        self.on_game_gui = True

        self.card_assets = []

        callback = {
        "select_color": self.select_color,
        "turn_changed": self.turn_changed
        }
        self.players = [Player("ME")]
        self.game = Game(self.players, callback)

        self.turn = self.game.turn()
        self.turn_changed()

    def select_color(self):
        print("SELECT COLOR")
        # TODO: Handle Select Color

    def turn_changed(self):
        card = self.game.table.top()
        if card.color:
            filename = card.color + "_" + card.card_type.split("_")[1]
        else:
            filename = "wild_" + card.card_type.split("_")[1]
        self.assets["table"].set_image(f"Material/Card/{filename}.png")

        self.card_assets = []
        for i, card in enumerate(self.players[0].hand):
            if card.color:
                filename = card.color + "_" + card.card_type.split("_")[1]
            else:
                filename = "wild_" + card.card_type.split("_")[1]
            self.card_assets.append(Asset(os.path.join(self.main.root_path, f"Material/Card/{filename}.png"), (30+i*100, 560), mag=0.2))


    def display(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.running = False
                
            if event.type == pygame.KEYDOWN:
                pass
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                self.collide_game(event.pos)
                pass
                
            if event.type == pygame.MOUSEMOTION:
                pass
            
        self.main.screen.blit(self.assets["background"].img, self.assets["background"].rect)

        if self.on_game_gui:
            self.draw_game()
            
    def draw_game(self):
        for name, asset in self.assets.items():
            self.main.screen.blit(asset.img, asset.rect)

        for card_asset in self.card_assets:
            self.main.screen.blit(card_asset.img, card_asset.rect)

        self.main.screen.blit(self.assets["table"].img, self.assets["table"].rect)

    def collide_game(self, mouse_pos):
        if self.assets["button_uno"].rect.collidepoint(mouse_pos):
            print("!")

        if self.assets["deck"].rect.collidepoint(mouse_pos):
            self.game.play(self.players[0])

        for i, card_asset in enumerate(self.card_assets):
            if card_asset.rect.collidepoint(mouse_pos):
                print(f"{i} card clicked")
                self.game.play(self.players[0], self.players[0].hand[i])
            
    def keydown_game(self, key):
        pass
    '''
        if(key == main.user_data.key_left):
            self.select_state -= 1
            return
        else:
            # 사용 가능한 키 보여주기
            return
        
        self.apply_state_change()
    '''
            
    def apply_state_change(self):
        # TODO: 현재 state에 따라 select 이미지 적절하게 이동시키기
        pass
    
    def enter_state(self, main):
        pass

    '''
        if(self.select_state == STATE_SINGLE_GAME):
            # TODO: 싱글 게임 시작 호출 
            pass
        elif(self.select_state == STATE_OPTION):
            self.on_title_gui = False
            # TODO: 옵션창 호출
            pass
        elif(self.select_state == STATE_EXIT):
            main.running = False
    '''