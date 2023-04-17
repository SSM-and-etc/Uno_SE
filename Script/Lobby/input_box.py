import pygame

class InputBox:
    def __init__(self, x, y, w, h, key,name):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('black')
        self.text = name
        self.active = False
        self.key=key
        # self.text_dict = {
        #     0:"player",
        #     1:"computer1",
        #     2:"computer2",
        #     3:"computer3",
        #     4:"computer4",
        #     5:"computer5",
        # }

    def handle_event(self, event):
        # for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
            #     # 마우스 클릭 위치가 Input Box 안에 있는지 확인합니다.
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
            if self.active == True:
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Enter 키를 누르면 Input Box의 텍스트를 출력합니다.
                            self.text= self.text
                        elif event.key == pygame.K_BACKSPACE:
                            # 백스페이스 키를 누르면 Input Box의 텍스트에서 마지막 문자를 삭제합니다.
                            self.text = self.text[:-1]
                        else:
                            # 키 입력이 있으면 Input Box의 텍스트에 추가합니다.
                            self.text += event.unicode

    def draw(self,screen):
        # Input Box와 텍스트를 화면에 그립니다.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

# Input Box를 생성합니다.
# input_boxes = [InputBox(0, 50, 200, 32,  0),
#                InputBox(50, 50, 200, 32,  1),
#                InputBox(50, 100, 200, 32, 2),
#                InputBox(50, 150, 200, 32, 3),
#                InputBox(50, 200, 200, 32, 4),
#                InputBox(50, 250, 200, 32, 5)]


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         for input_box in input_boxes:
#             input_box.handle_event(event)

#     for input_box in input_boxes:
#         input_box.draw(screen)
#     pygame.display.update()
