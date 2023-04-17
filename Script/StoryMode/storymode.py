import pygame

from System.option import Option

import random

import os


class Asset:
    design_size = (1280, 720)
    user_data = None

    def __init__(self, img, pos, mag=1.0):
        self.mag = mag
        self.pos = pos

        if isinstance(img, str):
            self.orig_img = pygame.image.load(img)
        else:
            self.orig_img = img.copy()
        self.img = pygame.transform.scale_by(self.orig_img, (self.mag, self.mag))

        self.rect = self.img.get_rect().move(pos)

    def set_image(self, img_path):
        self.orig_img = pygame.image.load(img_path)
        self.img = pygame.transform.scale_by(self.orig_img, (self.mag, self.mag))

        self.rect = self.img.get_rect().move(self.pos)

    def scaled_img(self):
        screen_size = self.user_data.get_screen_size()
        x_ratio, y_ratio = screen_size[0] / self.design_size[0], screen_size[1] / self.design_size[1]
        return pygame.transform.scale_by(self.orig_img, (self.mag * x_ratio, self.mag * y_ratio))

    def scaled_rect(self):
        screen_size = self.user_data.get_screen_size()
        x_ratio, y_ratio = screen_size[0] / self.design_size[0], screen_size[1] / self.design_size[1]

        x, y, w, h = self.rect
        x *= x_ratio
        w *= x_ratio
        y *= y_ratio
        h *= y_ratio
        return pygame.Rect(x, y, w, h) 

    def scaled(self):
        return self.scaled_img(), self.scaled_rect()

    def clone(self):
        asset = Asset(self.orig_img, self.pos, self.mag)
        asset.rect = self.rect.copy()
        return asset

    def copy(self, asset):
        self.mag = asset.mag
        self.pos = asset.pos
        self.img = asset.img.copy()
        self.rect = asset.rect

class FakeAsset(Asset):
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

class Selection:
    def __init__(self, popup, story_level):
        self.pos = 0
        self.story_level = story_level
        self.n = story_level
        self.popup = popup

    def reset(self):
        self.pos = 0
        if self.popup["visible"]:
            self.n = 1
        else:
            self.n = self.story_level

    def left(self):
        if self.pos > 0:
            self.pos -= 1

    def right(self):
        if self.pos < self.n:
            self.pos += 1

    def down(self):
        if self.pos < self.n:
            self.pos += 1

    def up(self):
        if self.pos > 0:
            self.pos -= 1

class StoryMode:
    def __init__(self, main):
        self.main = main
        self.user_data = main.user_data
        self.option = Option(main, self)
        self.on_option = False
        
        Asset.user_data = main.user_data
        
        self.assets = {
            "background": Asset(os.path.join(main.root_path, "Material/BG/map.png"), (0, 0)),
            "cursor": Asset(os.path.join(main.root_path, "Material/Button/button_cursor.png"), (-100, -100)),
        }

        self.level_name = ["europe", "asia", "america", "africa"]

        self.level_assets = [
            Asset(os.path.join(main.root_path, "Material/Avatar/europe.png"), (670, 80), mag=0.5),
            Asset(os.path.join(main.root_path, "Material/Avatar/asia.png"), (1050, 180), mag=0.5),
            Asset(os.path.join(main.root_path, "Material/Avatar/america.png"), (380, 350), mag=0.5),
            Asset(os.path.join(main.root_path, "Material/Avatar/africa.png"), (680, 400), mag=0.5),
        ]

        self.popup_assets = [
            Asset(os.path.join(main.root_path, "Material/Button/yes.png"), (480, 500), mag=0.5),
            Asset(os.path.join(main.root_path, "Material/Button/no.png"), (700, 500), mag=0.5),            
        ]

        self.popup = {
            "visible": False,
            "level": 0,
            "asset": Asset(os.path.join(main.root_path, "Material/GUI/pop_up.png"), (320, 120)),
        }

        self.level_description = [
            "현재 지역은 유럽입니다. 도전하시겠습니까?", 
            "현재 지역은 아시아입니다. 도전하시겠습니까?", 
            "현재 지역은 남아메리카입니다. 도전하시겠습니까?", 
            "현재 지역은 아프리카입니다. 도전하시겠습니까?"
        ]

        for i in range(4):
            if self.user_data.story_level < i:
                self.level_assets[i].set_image(os.path.join(main.root_path, f"Material/Avatar/{self.level_name[i]}_disabled.png"))
            
        self.on_game_gui = True

        self.description_font = pygame.font.SysFont("AppleGothic", 24)

        self.selection = Selection(self.popup, min(self.user_data.story_level, 3))

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
                    if self.collide_game(event.pos):
                        self.handle()
                    
                if event.type == pygame.MOUSEMOTION:
                    self.collide_game(event.pos)
                        
            if self.on_game_gui:
                self.draw_game()
    
    def move_cursor(self):
        sel = self.selection.pos
        asset = None

        if self.popup["visible"]:
            asset = self.popup_assets[sel]
        else:
            asset = self.level_assets[sel]

        pos_x = asset.rect.centerx - 10
        pos_y = asset.rect.top - 40
        self.assets["cursor"].rect.update(pos_x, pos_y, 0, 0)
            
    def draw_game(self):
        self.move_cursor()

        self.main.screen.blit(*self.assets["background"].scaled())

        for i in range(len(self.level_assets)-1):
            pygame.draw.line(self.main.screen, (255, 0, 0), self.level_assets[i].scaled_rect().center, self.level_assets[i+1].scaled_rect().center, 3)

        for level_asset in self.level_assets:
            self.main.screen.blit(*level_asset.scaled())

        if self.popup["visible"]:
            self.main.screen.blit(*self.popup["asset"].scaled())
            for popup_asset in self.popup_assets:
                self.main.screen.blit(*popup_asset.scaled())

            self.main.screen.blit(self.description_font.render(self.level_description[self.popup["level"]], True, (0, 0, 0)),
                                                               self.popup["asset"].scaled_rect().move(50, 50))

        self.main.screen.blit(*self.assets["cursor"].scaled())

    def collide_game(self, mouse_pos):
        if self.popup["visible"]:
            for i, popup_asset in enumerate(self.popup_assets):
                if popup_asset.scaled_rect().collidepoint(mouse_pos):
                    self.selection.pos = i
                    return True
        else:
            for i, level_asset in enumerate(self.level_assets):
                if level_asset.scaled_rect().collidepoint(mouse_pos):
                    self.selection.pos = i
                    return True
            
        return False

    def handle(self):
        sel = self.selection.pos
        if self.popup["visible"]:
            if sel == 0:
                self.main.stage_index = self.popup["level"]+1
                self.main.scene_change(self.main.get_scene_index("story mode game start"))
            elif sel == 1:
                self.popup["visible"] = False
                self.selection.reset()

        else:
            self.popup["visible"] = True
            self.popup["level"] = sel
            self.selection.reset()

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
    
    def change_screen_size(self):
        pass # title의 size 변경 방식과의 호환을 위해 임시로 만듦