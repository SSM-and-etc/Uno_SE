import pygame

class InputBox:
    def __init__(self, x, y, w, h, key,name,font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('black')
        self.namebox=['empty']
        self.active = False
        self.clicked= False
        if(name=='player0'):
            self.namebox.append('ME')
            self.clicked= True
            self.active = True
        else:
            self.namebox.append(name)    
        self.key=key
        self.font=font
        
    def handle_event(self, event):
        # for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
            #     # 마우스 클릭 위치가 Input Box 안에 있는지 확인합니다.
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                    self.clicked= not self.clicked
                else:
                    self.active=False
            if self.active == True:
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Enter 키를 누르면 Input Box의 텍스트를 출력합니다.
                            self.namebox[1]= self.namebox[1]
                        elif event.key == pygame.K_BACKSPACE:
                            # 백스페이스 키를 누르면 Input Box의 텍스트에서 마지막 문자를 삭제합니다.
                            self.namebox[1] = self.namebox[1][:-1]
                        else:
                            # 키 입력이 있으면 Input Box의 텍스트에 추가합니다.
                            self.namebox[1] += event.unicode

    def draw(self,screen):
        # Input Box와 텍스트를 화면에 그립니다.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # font = pygame.font.Font(None, int(self.screen_width/30))
        if(self.clicked==False):
            text_surface = self.font.render(self.namebox[0], True, self.color)
        else:
             text_surface = self.font.render(self.namebox[1], True, self.color)
        text_width, text_height = text_surface.get_size()
        center_x = self.rect.x + self.rect.width / 2
        center_y = self.rect.y + self.rect.height / 2
        screen.blit(text_surface, (center_x - text_width / 2, center_y - text_height / 2))


    
