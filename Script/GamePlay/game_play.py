import pygame

from uno.game import Game
from uno.player import Player
from uno.enums import CardColor, CardType
from Player.PlayerAI import PlayerAI

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

    def copy(self, asset):
        self.mag = asset.mag
        self.pos = asset.pos
        self.img = asset.img.copy()
        self.rect = asset.rect

class FakeAsset:
    def __init__(self, rect):
        self.rect = rect

class GamePlay:
    def __init__(self, main, stage_index, playerAI_number = 1):
        self.main = main
        self.stage_index = stage_index

        design_resolution = (1280, 720)
        screen_size = main.user_data.get_screen_size()

        self.assets = {
            "background": Asset(os.path.join(main.root_path, "Material/BG/game.png"), (0, 0)),
            "deck": Asset(os.path.join(main.root_path, "Material/Card/deck.png"), (180, 150), mag=0.3),
            "button_uno": Asset(os.path.join(main.root_path, "Material/Button/button_uno.png"), (610, 300)),
            "table": Asset(os.path.join(main.root_path, "Material/Card/deck.png"), (360, 150), mag=0.3),
            "color": Asset(os.path.join(main.root_path, "Material/Extra/red.png"), (610, 200))
        }

        self.on_game_gui = True

        self.card_assets = []
        self.animate_assets = []

        callback = {
        "select_color": self.select_color,
        "turn_changed": self.select_color 
        }

        self.player_setting(playerAI_number)
        self.game = Game(self.players, callback, stage_index)

        self.turn = self.game.turn()

        self.update_hand()
        self.update_table()

    def player_setting(self, playerAI_number):
        self.player = Player("ME")        
        self.players = [self.player]
        for _ in range(playerAI_number):
            self.players.append(PlayerAI(self.stage_index))


    def select_color(self):
        print("SELECT COLOR")
        return random.choice([CardColor.BLUE, CardColor.GREEN, CardColor.RED, CardColor.YELLOW])
        # TODO: Handle Select Color

    def update_table(self):
        card = self.game.table.top()
        if card.color:
            filename = card.color + "_" + card.card_type.split("_")[1]
        else:
            filename = "wild_" + card.card_type.split("_")[1]
        self.assets["table"].set_image(os.path.join(self.main.root_path, f"Material/Card/{filename}.png"))

        color = self.game.table.get_color()
        self.assets["color"].set_image(os.path.join(self.main.root_path, f"Material/Extra/{color}.png"))
        self.assets["deck2"] = Asset(os.path.join(self.main.root_path, "Material/Card/deck.png"), (180, 150), mag=0.3)

    def update_hand(self):
        self.card_assets = []
        for i, card in enumerate(self.player.hand):
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

    def animate_asset(self):
        if self.animate_assets:
            asset, dest, time, tick = self.animate_assets.pop()
            print(asset.rect, dest.rect, time, tick)

            if tick >= time:
                new_rect = dest.rect
                self.update_hand()
                self.update_table()

            else:
                new_rect = asset.pos[0] - ((asset.pos[0] - dest.rect[0]) * tick / time),\
                        asset.pos[1] - ((asset.pos[1] - dest.rect[1]) * tick / time),\
                        abs(asset.rect[2] - (asset.rect[2] - dest.rect[2]) / (time-tick)*5),\
                        abs(asset.rect[3] - (asset.rect[3] - dest.rect[3]) / (time-tick)*5),\
                        
                asset.img = pygame.transform.scale(asset.img, (new_rect[2], new_rect[3]))
                asset.rect.update(new_rect)
                
                self.animate_assets.append((asset, dest, time, tick+1))

            
    def draw_game(self):
        for name, asset in self.assets.items():
            self.main.screen.blit(asset.img, asset.rect)

        for card_asset in self.card_assets:
            self.main.screen.blit(card_asset.img, card_asset.rect)

        self.animate_asset()

        self.main.screen.blit(self.assets["table"].img, self.assets["table"].rect)

    def collide_game(self, mouse_pos):
        if self.assets["button_uno"].rect.collidepoint(mouse_pos):
            print("!")

        if self.assets["deck"].rect.collidepoint(mouse_pos):
            self.animate_assets.append((self.assets["deck2"], self.card_assets[-1], 50, 0))
            self.game.play(self.player)

        for i, card_asset in enumerate(self.card_assets):
            if card_asset.rect.collidepoint(mouse_pos):
                print(f"{i} card clicked")
                if self.game.table.playable(self.players[0].hand[i]):
                    self.animate_assets.append((card_asset, self.assets["table"], 50, 0))
                    self.game.play(self.player, self.player.hand[i])

                    

            
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