import pygame

class UserData():
    def __init__(self):
        # if 기존 save파일이 있을 경우:
        #   self.load_data()
        # else:
            self.reset_data()
            # self.save_data()
        
        
    def load_data(self):
        pass
    
    def save_data(self):
        pass
    
    def reset_data(self):
        self.screen_width        =   1280
        self.screen_height       =   720
        
    def get_screen_size(self):
        return (self.screen_width, self.screen_height)