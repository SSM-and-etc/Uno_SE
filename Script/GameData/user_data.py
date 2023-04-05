import pygame

class DataSet():
    def __init__(self):
        self.json_object = \
            {
                "screen_size_index" : 1
            }

class UserData():
    def __init__(self):
        # if 기존 save파일이 있을 경우:
        #   self.load_data()
        # else:
        self.reset_data()
            # self.save_data()
        
        
        self.screen_sizes = [(640, 480), (1280, 720), (1920, 1080), (2560,1440)]
        
        
    def load_data(self):
        pass
    
    def save_data(self):
        pass
    
    def reset_data(self):
        self.screen_width        =   1280
        self.screen_height       =   720
        self.key_left            =  pygame.K_LEFT
        self.key_right            =  pygame.K_RIGHT
        self.key_enter            =  pygame.K_RETURN
        
    def get_screen_size(self):
        return (self.screen_width, self.screen_height)
    
    def set_screen_size(self, screen_size_index):
        self.screen_width, self.screen_height = self.screen_sizes[screen_size_index]