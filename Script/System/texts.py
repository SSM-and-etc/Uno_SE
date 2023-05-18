import pygame

COLORS = {"BLUE_MAGENTA" : (153, 102, 204)} # color.py 따로 작성하는 것이 좋아 보임


class Texts():
    def __init__(self, data):
        self.user_data = data
        self.default_sizes = []
        self.default_texts = []
        self.texts = []
        self.default_poses = []
        self.poses = []
        self.colors = []
        self.font_names = []
        self.design_size = (1280,720)
        
    def draw(self, screen):
        for i in range(len(self.texts)):
            screen.blit(self.texts[i], self.poses[i])
            
    def add(self, text, pos, size = 30, font_name = "arial", font_color = "BLUE_MAGENTA"):
        self.default_texts.append(text)
        self.default_poses.append(pos)
        self.default_sizes.append(size)
        self.colors.append(COLORS[font_color])
        self.font_names.append(font_name)
        
        i = len(self.default_poses) - 1
        self.apply_pos_scale(i)
        self.apply_text_scale(i, self.get_font_ratio())
        
    def change_text(self, i, text, size = 30, font_name = "arial", font_color = "BLUE_MAGENTA"):
        self.default_texts[i] = text
        self.default_sizes[i] = size
        self.colors[i] = COLORS[font_color]
        self.font_names[i] = font_name
        self.apply_text_scale(i, self.get_font_ratio())
        
    def apply_text_scale(self, i, font_ratio):
        font = pygame.font.SysFont(self.font_names[i], self.default_sizes[i] * font_ratio, True, True)
        self.texts[i] = font.render(self.default_texts[i], True, self.colors[i])
        
    def apply_pos_scale(self, i):
        self.poses[i] = self.tup_mul(self.user_data.get_screen_size(), self.default_poses[i])
        
    def apply_screen_size(self):
        font_ratio = self.get_font_ratio()
        for i in range(len(self.texts)):
            self.apply_pos_scale(i)
            self.apply_text_scale(i, font_ratio)
        
    def get_font_ratio(self):
        screen_size = self.user_data.get_screen_size()
        return (screen_size[0]/self.design_size[0] + screen_size[1]/self.design_size[1]) / 2
        
    def tup_mul(self, tup1, tup2):
        return (tup1[0] * tup2[0], tup1[1] * tup2[1])
    
    def tup_div(self, tup1, tup2):
        return (tup1[0] / tup2[0], tup1[1] / tup2[1])