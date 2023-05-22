import pygame

from System.images import Images
from System.statebuttons import StateButtons
from System.texts import Texts

Achievements_scripts = [[("First win" , "Win a Single Player Battle"),("Africa win" , "Win story mode area 1"),("America win" , "Win story mode area 2"),("Asia win" , "Win story mode area 3")],[("Europe win" , "Win story mode area 4"),("Fast win" , "Win in 10 turns in a single player game"),("Fair" , "Win without ever using a skill card"),("Uno dos" , "Win after the other player declares uno")],[("Perfect win" , "Win with 10 or more cards in your opponent's hand in a single player game"),("3 combo" , "Play 3 cards in a row."),("tajja" , "When only skill cards are collected in the first draw"),("lucky guy" , "Win without a draw except for the first throw")]]
Achievements_path = [[("Material/Challenge/first_win.png", "Material/Challenge/first_win.png"),("Material/Challenge/africa_win.png", "Material/Challenge/africa_win.png"),("Material/Challenge/america_win.png", "Material/Challenge/america_win.png"),("Material/Challenge/asia_win.png", "Material/Challenge/asia_win.png")],[("Material/Challenge/europe_win.png", "Material/Challenge/europe_win.png"),("Material/Challenge/fast_win.png", "Material/Challenge/fast_win.png"),("Material/Challenge/fair.png", "Material/Challenge/fair.png"),("Material/Challenge/uno_dos.png", "Material/Challenge/uno_dos.png")],[("Material/Challenge/perfect_win.png", "Material/Challenge/perfect_win.png"),("Material/Challenge/3_combo.png", "Material/Challenge/3_combo.png"),("Material/Challenge/tajja.png", "Material/Challenge/tajja.png"),("Material/Challenge/lucky_guy.png", "Material/Challenge/lucky_guy.png")]]
Achievements_path_c = [[("Material/ColorMode/Challenge/first_win.png", "Material/ColorMode/Challenge/first_win.png"),("Material/ColorMode/Challenge/africa_win.png", "Material/ColorMode/Challenge/africa_win.png"),("Material/ColorMode/Challenge/america_win.png", "Material/ColorMode/Challenge/america_win.png"),("Material/ColorMode/Challenge/asia_win.png", "Material/ColorMode/Challenge/asia_win.png")],[("Material/ColorMode/Challenge/europe_win.png", "Material/ColorMode/Challenge/europe_win.png"),("Material/ColorMode/Challenge/fast_win.png", "Material/ColorMode/Challenge/fast_win.png"),("Material/ColorMode/Challenge/fair.png", "Material/ColorMode/Challenge/fair.png"),("Material/ColorMode/Challenge/uno_dos.png", "Material/ColorMode/Challenge/uno_dos.png")],[("Material/ColorMode/Challenge/perfect_win.png", "Material/ColorMode/Challenge/perfect_win.png"),("Material/ColorMode/Challenge/3_combo.png", "Material/ColorMode/Challenge/3_combo.png"),("Material/ColorMode/Challenge/tajja.png", "Material/ColorMode/Challenge/tajja.png"),("Material/ColorMode/Challenge/lucky_guy.png", "Material/ColorMode/Challenge/lucky_guy.png")]]
Achievements_None_path = "Material/Challenge/None.png"
Achievements_None_path_c = "Material/ColorMode/Challenge/None.png"

class Achievements():
    def __init__(self, main):
        self.main = main
        self.user_data = main.user_data
        self.BG = StateButtons(main.user_data, main.root_path, (1280, 720), False)
        self.buttons = StateButtons(main.user_data, main.root_path, (19200, 10800))
        self.texts = Texts(main.user_data)
        self.now_achi_imgs = Images(main.user_data, main.root_path, (12800, 7200))
        self.now_achi_texts = Texts(main.user_data)
        
        self.comp_imgs = Images(main.user_data, main.root_path, (19200, 10800))
        self.comp_texts = Texts(main.user_data)
        
        self.add_assets()
        self.default_font_size = 20
        self.apply_check()
        
        
    def display(self, main):
        self.draw(main.screen)
        self.on_achievements = True
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main.running = False
                    
                if event.type == pygame.KEYDOWN:
                    self.keydown(main, event.key)
                
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.click_collide(main, event.pos)
                    
                if event.type == pygame.MOUSEMOTION:
                    self.move_collide(main, event.pos)
        
        return self.on_achievements
    
    def draw(self, screen):
        self.BG.draw(screen)
        self.now_achi_imgs.draw(screen)
        self.buttons.draw(screen)
        self.texts.draw(screen)
        self.now_achi_texts.draw(screen)
        
    def comp_draw(self, screen):
        self.comp_imgs.draw(screen)
        self.comp_texts.draw(screen)
        
    def set_comp(self, index):
        i, j = divmod(index, len(self.buttons.imgs[0]))
        print((i, j))
        self.comp_imgs.change_img(0, 0, self.buttons.get_img(i, j))
        self.comp_texts.change_text(0, Achievements_scripts[i][j][0])
        
    def keydown(self, main, key):
        if not self.buttons.key_down_state(key):
            match key:
                case self.user_data.key_enter:
                    self.change_achi()
                case pygame.K_ESCAPE:
                    self.exit()
            
    def click_collide(self, main, mouse_pos):
        if not self.BG.get_clicked_button_idx(mouse_pos):
            self.exit()
        clicked_button_idx = self.buttons.get_clicked_button_idx(mouse_pos)
        if clicked_button_idx:
            self.change_achi()
        
    def move_collide(self, main, mouse_pos):
        self.buttons.get_clicked_button_idx(mouse_pos)
        
    def add_assets(self):
        self.add_imgs()
        self.add_buttons()
        self.add_texts()
        
    def apply_screen_size(self):
        self.BG.apply_screen_size()
        self.now_achi_imgs.apply_screen_size()
        self.buttons.apply_screen_size()
        self.now_achi_texts.apply_screen_size()
        #self.imgs.apply_screen_size()
        
    def add_imgs(self):
        self.now_achi_imgs.add_row(Achievements_None_path, Achievements_None_path_c, (0.3, 0.67))
        self.comp_imgs.add_row(Achievements_None_path, Achievements_None_path_c, (0.45, 0.1))
        
    def add_buttons(self):
        self.BG.add_row("Material/GUI/pop_up.png", "Material/ColorMode/GUI/pop_up.png", (0.5, 0.5))
        for i in range(len(Achievements_path)):
            self.buttons.add_row(Achievements_None_path, Achievements_None_path_c, (0, 0), Achievements_path[i][0][0], Achievements_path_c[i][0][1])
            self.buttons.set_checked(i, 0, self.user_data.achievements[i * len(Achievements_path[0])][0])
            for j in range(1, len(Achievements_path[i])):
                self.buttons.add(Achievements_None_path, Achievements_None_path_c, (0, 0), Achievements_path[i][j][0], Achievements_path_c[i][j][1])
                self.buttons.set_checked(i, j, self.user_data.achievements[i * len(Achievements_path[0]) + j][0])
        for i in range(len(self.buttons.imgs)):
            self.buttons.set_row_linspace(i, 0.25, 0.75)
        for j in range(len(self.buttons.imgs[0])):
            self.buttons.set_col_linspace(j, 0.15, 0.65)
        
    def add_texts(self):
        self.now_achi_texts.add("-", (0.35, 0.6), 30, "arial", "BLUE_GREEN")
        self.now_achi_texts.add("-", (0.35, 0.67), 15, "arial", "BLACK", "BLACK")
        self.now_achi_texts.add("--.--.--", (0.275, 0.73), 20, "arial", "VERMILION", "VERMILION")
        self.comp_texts.add("", (0.5, 0.07), 30, "arial", "REDDISH_PURPLE", "VERMILION")
        
    def apply_check(self):
        for i in range(len(Achievements_path)):
            for j in range(len(Achievements_path[i])):
                self.buttons.set_checked(i, j, self.user_data.achievements[i * len(Achievements_path[0]) + j][0])
        self.comp_imgs.set_checked(0, 0, True)
        
    def change_achi(self):
        i, j = self.buttons.get_state()
        is_on, date = self.user_data.achievements[i * len(Achievements_path[0]) + j]
        self.now_achi_imgs.change_img(0, 0, self.buttons.get_img(i, j))
        self.now_achi_imgs.set_checked(0, 0, is_on)
        self.now_achi_texts.change_text(0, Achievements_scripts[i][j][0])
        self.now_achi_texts.change_text(1, Achievements_scripts[i][j][1])
        self.now_achi_texts.change_text(2, date)
    
    def exit(self):
        self.on_achievements = False
