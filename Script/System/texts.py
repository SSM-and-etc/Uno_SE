import pygame

COLORS = \
{
    "BLUE_MAGENTA"      : (153, 102, 204), 
    "REDDISH_PURPLE"    : (149, 53, 83),
    "SKY_BLUE"          : (135,206,235),
    "BLACK"             : (0, 0, 0),
    "ORANGE"            : (255, 165, 0),
    "BLUE_GREEN"        : (13, 152, 186),
    "YELLOW"            : (255,255,0),
    "BLUE"              : (0, 0, 255),
    "VERMILION"         : (227, 66, 52)
}


class Texts():
    def __init__(self, data):
        self.user_data = data
        self.default_sizes = []
        self.default_texts = []
        self.texts = []
        self.texts_c = []
        self.default_poses = []
        self.poses = []
        self.colors = []
        self.colors_c = []
        self.font_names = []
        self.design_size = (1280,720)
        
        self.is_off = False
        
    def draw(self, screen):
        if self.is_off:
            return
        
        if self.user_data.color_blindness_mode:
            for i in range(len(self.texts)):
                screen.blit(self.texts_c[i], self.poses[i])
        else:
            for i in range(len(self.texts)):
                screen.blit(self.texts[i], self.poses[i])
                
    def get_text_data(self, i):
        return (self.texts[i], self.poses[i]), (self.texts_c[i], self.poses[i])
    
    def get_only_text(self, i):
        return self.default_texts[i]
            
    def add(self, text, pos, size = 30, font_name = "arial", font_color = "BLUE_MAGENTA", font_color_c = "REDDISH_PURPLE"):
        self.default_texts.append(text)
        self.default_poses.append(pos)
        self.default_sizes.append(size)
        self.colors.append(COLORS[font_color])
        self.colors_c.append(COLORS[font_color_c])
        self.font_names.append(font_name)
        self.poses.append(None)
        self.texts.append(None)
        self.texts_c.append(None)
        
        i = len(self.default_poses) - 1
        self.apply_pos_scale(i)
        self.apply_text_scale(i, self.get_font_ratio())
        
    def change_text(self, i, text):
        self.default_texts[i] = text
        self.apply_text_scale(i, self.get_font_ratio())
        self.apply_pos_scale(i)
        
    def change_text_all(self, i, text, size = 30, font_name = "arial", font_color = "BLUE_MAGENTA", font_color_c = "REDDISH_PURPLE"):
        self.default_texts[i] = text
        self.default_sizes[i] = size
        self.colors[i] = COLORS[font_color]
        self.colors_c[i] = COLORS[font_color_c]
        self.font_names[i] = font_name
        self.apply_text_scale(i, self.get_font_ratio())
        self.apply_pos_scale(i)
        
    def apply_text_scale(self, i, font_ratio):
        font = pygame.font.SysFont(self.font_names[i], int(self.default_sizes[i] * font_ratio), True, True)
        self.texts[i] = font.render(self.default_texts[i], True, self.colors[i])
        self.texts_c[i] = font.render(self.default_texts[i], True, self.colors_c[i])
        
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
    
    def reset(self):
        for i in range(len(self.texts)):
            self.change_text(i, "")