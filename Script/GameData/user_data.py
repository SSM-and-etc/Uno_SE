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
        self.screen_size_index = 1
        
        
    def load_data(self):
        pass
    
    def save_data(self, main):
        self.set_screen_size(main, self.screen_size_index)
        main.set_screen()
    
    def reset_data(self):
        self.screen_width           = 1280
        self.screen_height          = 720
        self.key_left               = pygame.K_LEFT
        self.key_right              = pygame.K_RIGHT
        self.key_enter              = pygame.K_RETURN
        self.key_up                 = pygame.K_UP
        self.key_down               = pygame.K_DOWN
        self.color_blindness_mode   = False
        self.volumes                = [1, 1, 1] # master, bgm, eft 순서 0 ~ 1?
        self.volumes_off            = [False, False, False] # 위와 동일
        self.screen_size_index = 1
        self.story_level = 0
        
    def get_screen_size(self):
        return self.screen_sizes[self.screen_size_index]
    
    def set_screen_size(self, main, screen_size_index):
        self.screen_size_index = screen_size_index
        self.screen_width, self.screen_height = self.screen_sizes[screen_size_index]
        
    def set_key(self, key_index, new_key):
        match key_index:
            case 0:
                self.key_left = new_key
            case 1:
                self.key_right = new_key
            case 2:
                self.key_enter = new_key
            case 3:
                self.key_up = new_key
            case 4:
                self.key_down = new_key
                
    def copy_data(self, other_data):
        # TODO: 노가다 말고 뭔가 좋은 방법이 없을까..?
        # 단일 변수 아닌 애들은 깊은 복사 안 되게 조정
        self.screen_width           = other_data.screen_width        
        self.screen_height          = other_data.screen_height       
        self.key_left               = other_data.key_left            
        self.key_right              = other_data.key_right           
        self.key_enter              = other_data.key_enter           
        self.key_up                 = other_data.key_up              
        self.key_down               = other_data.key_down            
        self.color_blindness_mode   = other_data.color_blindness_mode
        self.volumes                = [i for i in other_data.volumes]
        self.volumes_off            = [i for i in other_data.volumes_off]   
        self.screen_size_index = other_data.screen_size_index
        self.story_level = other_data.story_level