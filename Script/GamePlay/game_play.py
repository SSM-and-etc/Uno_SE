import pygame

from uno.game import Game
from uno.player import Player
from uno.enums import CardColor, CardType
from Player.PlayerAI import PlayerAI
from System.option import Option

import random

import os


class Asset:
    def __init__(self, img_path, pos, mag=1.0):
        self.mag = (mag, mag)
        self.pos = pos

        self.orig_img = pygame.image.load(img_path)
        self.img = pygame.transform.scale_by(self.orig_img, self.mag)

        self.rect = self.img.get_rect().move(pos)

    def set_image(self, img_path):
        self.orig_img = pygame.image.load(img_path)
        self.img = pygame.transform.scale_by(self.orig_img, self.mag)

        self.rect = self.img.get_rect().move(self.pos)

    def copy(self, asset):
        self.mag = asset.mag
        self.pos = asset.pos
        self.img = asset.img.copy()
        self.rect = asset.rect

class FakeAsset:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

class Selection:
    def __init__(self, player, color_selection):
        self.map = [
            ["deck", "button_uno"],
            list(CardColor),
            ["card"]
        ]
        self.pos = [2, 0] # card[0]
        self.player = player
        self.color_selection = color_selection

    def reset(self):
        self.pos = [2, 0]

    def current(self):
        if self.pos[0] == 2:
            return "card", self.pos[1]

        else:
            return self.map[self.pos[0]][self.pos[1]], 0

    def set(self, obj, idx=0):
        if obj == "card":
            self.pos = [2, idx]

        else:
            for i, row in enumerate(self.map):
                for j, col in enumerate(row):
                    if col == obj:
                        self.pos = [i, j]
                        return

    def left(self):
        if self.pos[1] > 0:
            self.pos[1] -= 1

    def right(self):
        if self.pos[0] == 2:
            if self.pos[1] < len(self.player.hand)-1:
                self.pos[1] += 1
        else:
            if self.pos[1] < len(self.map[self.pos[0]])-1:
                self.pos[1] += 1

    def down(self):
        if self.pos[0] < 2:
            self.pos[0] += 1
            self.pos[1] = 0

        if self.pos[0] == 1 and not self.color_selection["selecting"]:
            self.pos[0] = 2

    def up(self):
        if self.pos[0] > 0:
            self.pos[0] -= 1
            self.pos[1] = 0

        if self.pos[0] == 1 and not self.color_selection["selecting"]:
            self.pos[0] = 0

class GamePlay:
    def __init__(self, main, stage_index = 1, playerAI_number = 1):
        self.main = main
        self.stage_index = stage_index
        self.user_data = main.user_data
        self.option = Option(main)
        self.on_option = False
        self.turn_count_gimmick = 1
        self.user_turn_count_gimmick = 1
        self.color_selection = {
            "selecting": False,
            "idx": None,
            "assets": {CardColor.RED: Asset(os.path.join(main.root_path, "Material/Extra/red.png"), (200, 400)),
                        CardColor.GREEN: Asset(os.path.join(main.root_path, "Material/Extra/green.png"), (300, 400)),
                        CardColor.BLUE: Asset(os.path.join(main.root_path, "Material/Extra/blue.png"), (400, 400)),
                        CardColor.YELLOW: Asset(os.path.join(main.root_path, "Material/Extra/yellow.png"), (500, 400))
            }
        }

        design_resolution = (1280, 720)
        screen_size = main.user_data.get_screen_size()

        self.assets = {
            "background": Asset(os.path.join(main.root_path, "Material/BG/game.png"), (0, 0)),
            "deck": Asset(os.path.join(main.root_path, "Material/Card/deck.png"), (180, 150), mag=0.3),
            "button_uno": Asset(os.path.join(main.root_path, "Material/Button/button_uno.png"), (600, 250)),
            "table": Asset(os.path.join(main.root_path, "Material/Card/deck.png"), (380, 150), mag=0.3),
            "color": Asset(os.path.join(main.root_path, "Material/Extra/red.png"), (625, 150)),
            "cursor": Asset(os.path.join(main.root_path, "Material/Button/button_cursor.png"), (-100, -100))
        }

        self.on_game_gui = True

        self.card_assets = []
        self.animate_assets = []

        self.counter_font = pygame.font.SysFont(None, 50)
        self.name_font = pygame.font.SysFont(None, 50)

        self.player_setting(playerAI_number)
        self.game = Game(self.players, stage_index)

        self.pane_assets = [FakeAsset((10, 514, 876, 196))]
        for i in range(len(self.players)-1):
            self.pane_assets.append(Asset(os.path.join(main.root_path, "Material/BG/player_panel.png"), (906, 10 + 150 * i)))

        self.selection = Selection(self.player, self.color_selection)

        self.update_hand()
        self.update_table()    

    def player_setting(self, playerAI_number):
        self.player = Player("ME")        
        self.players = [self.player]
        if self.stage_index != 0:
            playerAI_number = self.player_ai_setting()
        for _ in range(playerAI_number):
            self.players.append(PlayerAI(self.stage_index))

    def player_ai_setting(self): # 스테이지별 ai 수 조정
        match self.stage_index:
            case 1:
                return 1
            case 2:
                return 3
            case 3:
                return 2
            case 4:
                return 2
            case _:
                return None
            
    def update_table(self):
        card = self.game.table.top()
        if card.is_color():
            filename = card.color + "_" + card.card_type.split("_")[1]
        else:
            filename = "wild_" + card.card_type.split("_")[1]
        self.assets["table"].set_image(os.path.join(self.main.root_path, f"Material/Card/{filename}.png"))

        color = self.game.table.get_color()
        self.assets["color"].set_image(os.path.join(self.main.root_path, f"Material/Extra/{color}.png"))
        self.assets["deck2"] = Asset(os.path.join(self.main.root_path, "Material/Card/deck.png"), (180, 150), mag=0.3)

        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.counter = 15

    def calculate_card_size(self, player_num):
        n = len(self.game.players[player_num].hand)

        pane_asset = self.pane_assets[player_num]
        pane_x, pane_y, pane_w, pane_h = pane_asset.rect

        card_orig = 388, 562

        card_x = (pane_w - 20) / n
        mag = card_x / card_orig[0]
        card_h = card_orig[1] * mag

        if card_h > (pane_h - 20) * 0.8:
            card_h = (pane_h - 20) * 0.8
            mag = card_h / card_orig[1]
            card_x = card_orig[0] * mag

        return card_x, pane_y + (pane_h-card_h) / 2, mag * 0.9

    def update_hand(self):
        card_size = self.calculate_card_size(0)

        self.card_assets = []
        for i, card in enumerate(self.player.hand):
            if card.is_color():
                filename = card.color + "_" + card.card_type.split("_")[1]
            else:
                filename = "wild_" + card.card_type.split("_")[1]
            self.card_assets.append(Asset(os.path.join(self.main.root_path, f"Material/Card/{filename}.png"), (10+card_size[0]*i, 30+card_size[1]), mag=card_size[2]))
            
        if self.color_selection["selecting"]:
            self.color_selection["selecting"] = False

        self.selection.reset()


    def display(self, main):
        if self.on_option:
            self.on_option = self.option.display(main)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main.running = False
                    
                if event.type == pygame.KEYDOWN:
                    self.keydown_game(main, event.key)
                
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if not self.game.table.top().is_special():
                        self.collide_game(event.pos)
                        self.handle()
                    
                if event.type == pygame.MOUSEMOTION:
                    if not self.game.table.top().is_special():
                        self.collide_game(event.pos)
                
                if event.type == pygame.USEREVENT and self.counter > 0:
                    self.counter_event()
                        
            self.main.screen.blit(self.assets["background"].img, self.assets["background"].rect)

            if self.on_game_gui:
                self.draw_game()
    
    def counter_event(self):
        if self.counter > 0:
            self.counter -= 1

        if self.game.table.top().is_special():
            card = self.game.table.top()

            if card.card_type == CardType.CARD_CHANGECOLOR:
                card.color = random.choice(list(CardColor))
            self.game.turn().hand.append(card)
            self.game.play(self.game.turn(), len(self.players), card)
            self.animate_assets.append((self.assets["deck2"], self.assets["table"], 50, 0, False))
            self.game.table.put(self.game.deck.draw())

        if self.counter == 0:
            #pygame.time.set_timer(pygame.USEREVENT, 0)
            self.animate_assets.append((self.assets["deck2"], self.card_assets[-1], 50, 0, True))
            self.play_player(self.game.turn())  
        
        elif self.counter == 12 and self.player != self.game.turn(): # AI Player
            #pygame.time.set_timer(pygame.USEREVENT, 0)
            card = self.game.turn().choose_card(self.game.table) # self.game.turn() is ai player

            if card: # deal
                if card.is_color():
                    filename = card.color + "_" + card.card_type.split("_")[1]
                else:
                    filename = "wild_" + card.card_type.split("_")[1]
                pos_x, pos_y, _, _ = self.pane_assets[self.game.players.index(self.game.turn())].rect
                asset = Asset(os.path.join(self.main.root_path, f"Material/Card/{filename}.png"), (pos_x, pos_y), mag=0.3)
                self.animate_assets.append((asset, self.assets["table"], 50, 0, True))

                if card.card_type == CardType.CARD_CHANGECOLOR:
                    card.color = self.game.turn().choose_color(self.game.table.get_color())
            else: # draw
                self.animate_assets.append((self.assets["deck2"], self.pane_assets[self.game.players.index(self.game.turn())], 50, 0, False))
            
            self.play_player(self.game.turn(), card)

    def play_player(self, player, card = None):
        # self.game.play() 이후의 self.game.turn()은 순서를 넘겨 받은 플레이어가 됨에 주의
        self.counter = 0
        self.game.play(player, len(self.players), card)
        self.turn_count_gimmick += 1
        if self.game.turn() == self.player:
            self.user_turn_count_gimmick += 1
        
        match self.stage_index:
            case 3:
                while self.turn_count_gimmick >= 5:
                    self.turn_count_gimmick -= 5
                    print("stage 3 기믹")
                    self.select_color()
            case 4:
                if self.game.turn() == self.player and not (self.user_turn_count_gimmick & 1):
                    print("stage 4 드로우 기믹")
                    self.game.draw(self.game.turn(), 2)
                if self.turn_count_gimmick == 5:
                    print("stage 4 패 교환 기믹")
                    self.game.hand_swap(player, self.game.turn())
                    self.turn_count_gimmick = 0
                    
    def animate_asset(self):
        if self.animate_assets:
            asset, dest, time, tick, resize = self.animate_assets.pop()

            if tick >= time:
                new_rect = dest.rect
                self.update_hand()
                self.update_table()

            else:
                new_rect = asset.pos[0] - ((asset.pos[0] - dest.rect[0]) * tick / time),\
                        asset.pos[1] - ((asset.pos[1] - dest.rect[1]) * tick / time),\
                        abs(asset.rect[2] - (asset.rect[2] - dest.rect[2]) / (time-tick)*5),\
                        abs(asset.rect[3] - (asset.rect[3] - dest.rect[3]) / (time-tick)*5),\
                        
                if resize:
                    asset.img = pygame.transform.scale(asset.img, (new_rect[2], new_rect[3]))
                asset.rect.update(new_rect)
                
                self.animate_assets.append((asset, dest, time, tick+1, resize))

    def move_cursor(self):
        sel, idx = self.selection.current()
        asset = None
        if sel == "card":
            asset = self.card_assets[idx]
        elif isinstance(sel, CardColor):
            asset = self.color_selection["assets"][sel]
        else:
            asset = self.assets[sel]

        pos_x = asset.rect.centerx - 10
        pos_y = asset.rect.top - 40
        self.assets["cursor"].rect.update(pos_x, pos_y, 0, 0)
            
    def draw_game(self):
        self.animate_asset()
        self.move_cursor()

        for name, asset in self.assets.items():
            self.main.screen.blit(asset.img, asset.rect)

        for card_asset in self.card_assets:
            self.main.screen.blit(card_asset.img, card_asset.rect)

        for i, pane_asset in enumerate(self.pane_assets):
            if i != 0:
                self.main.screen.blit(pane_asset.img, pane_asset.rect)
                w, y, mag = self.calculate_card_size(i)
                for j in range(len(self.game.players[i].hand)):
                    img = pygame.transform.scale_by(self.assets["deck"].orig_img, mag)
                    self.main.screen.blit(img, (10 + pane_asset.rect[0] + w*j, 30 + y))

            self.main.screen.blit(self.name_font.render(self.game.players[i].tag, True, (255, 255, 255)), pane_asset.rect.move(5, 5))

            if self.game.players[i] == self.game.turn():
                pygame.draw.rect(self.main.screen, (255, 0, 0), pane_asset, 2)

        for asset in self.animate_assets:
            self.main.screen.blit(asset[0].img, asset[0].rect)

        if self.color_selection["selecting"]:
            for color, asset in self.color_selection["assets"].items():
                self.main.screen.blit(asset.img, asset.rect)

        if self.game.uno_player:
            self.main.screen.blit(self.name_font.render(self.game.uno_player.tag, True, (255, 255, 255)), self.assets["button_uno"].rect.move(0, 75))

        self.main.screen.blit(self.assets["table"].img, self.assets["table"].rect)
        self.main.screen.blit(self.counter_font.render(str(self.counter), True, (255, 255, 255)), (830, 450))

    def collide_game(self, mouse_pos):
        if self.assets["button_uno"].rect.collidepoint(mouse_pos):
            self.selection.set("button_uno")

        if self.assets["deck"].rect.collidepoint(mouse_pos):
            self.selection.set("deck")

        for i, card_asset in enumerate(self.card_assets):
            if card_asset.rect.collidepoint(mouse_pos):
                self.selection.set("card", i)

        if self.color_selection["selecting"]:
            for color, asset in self.color_selection["assets"].items():
                if asset.rect.collidepoint(mouse_pos):
                    self.selection.set(color)
        
    def handle(self):
        sel, idx = self.selection.current()

        if sel == "card":
            if self.game.turn() == self.player:
                if idx < len(self.player.hand) and self.game.table.playable(self.player.hand[idx]):
                    if self.player.hand[idx].card_type == CardType.CARD_CHANGECOLOR:
                        self.color_selection["selecting"] = True
                        self.color_selection["idx"] = idx

                    else:
                        self.animate_assets.append((self.card_assets[idx], self.assets["table"], 50, 0, True))
                        self.play_player(self.player, self.player.hand[idx])    

        elif sel == "deck":
            if self.game.turn() == self.player:
                self.animate_assets.append((self.assets["deck2"], self.card_assets[-1], 50, 0, True))
                self.play_player(self.player)

        elif sel == "button_uno":
            self.assets["button_uno"].set_image(os.path.join(self.main.root_path, "Material/Button/button_uno_enabled.png"))
            self.game.uno_player = self.player
            print("uno!")

        elif isinstance(sel, CardColor):
            self.player.hand[self.color_selection["idx"]].color = sel

            self.animate_assets.append((self.card_assets[self.color_selection["idx"]], self.assets["table"], 50, 0, True))
            self.play_player(self.player, self.player.hand[self.color_selection["idx"]])

            self.color_selection["selecting"] = False
    
    def keydown_game(self, main, key):
        if key == self.user_data.key_left:
            self.selection.left()
        elif key == self.user_data.key_right:
            self.selection.right()
        elif key == self.user_data.key_up:
            self.selection.up()
        elif key == self.user_data.key_down:
            self.selection.down()
        elif key == self.user_data.key_enter:
            self.handle()
        elif key == pygame.K_ESCAPE:
            self.on_option = True
            
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