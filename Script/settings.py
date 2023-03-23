import pygame
import sys
from pygame.locals import *

pygame.init()

sizeofscreen=(640,480)
screen = pygame.display.set_mode(sizeofscreen)

pygame.display.set_caption('Settings')
font = pygame.font.SysFont('applegothic', 30)

is_colormode=0


def colormode(is_colormode):
    if is_colormode == 0 :
        return

    elif is_colormode == 1 :
        return

def resize_window(width, height):
    pygame.display.set_mode((width, height))

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.SysFont('applegothic', 30)
        self.rendered_text = self.font.render(self.text, True, pygame.Color('white'))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered_text, (self.rect.x + self.rect.width / 2 - self.rendered_text.get_width() / 2,
                                          self.rect.y + self.rect.height / 2 - self.rendered_text.get_height() / 2))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

screen_size = pygame.display.set_mode(sizeofscreen)
pygame.display.flip()

screen_keysetting = pygame.display.set_mode(sizeofscreen)
pygame.display.flip()

screen_colormode = pygame.display.set_mode(sizeofscreen)
pygame.display.flip()

screen_reset = pygame.display.set_mode(sizeofscreen)
pygame.display.flip()

button_width, button_height = 240, 50

button_size = Button(sizeofscreen[0] // 2 - button_width // 2, 20, button_width, button_height, "화면 크기 설정", pygame.Color('blue'), pygame.Color('lightblue'))
button_keysetting= Button(sizeofscreen[0] // 2 - button_width // 2, 120, button_width, button_height, "키 설정 변경", pygame.Color('green'), pygame.Color('lightgreen'))
button_colormode = Button(sizeofscreen[0] // 2 - button_width // 2, 220, button_width, button_height, "색약모드 on/off", pygame.Color('red'), pygame.Color('salmon'))
button_settingreset = Button(sizeofscreen[0] // 2 - button_width // 2, 320, button_width, button_height, "설정 초기화", pygame.Color('purple'), pygame.Color('plum'))
button_save = Button(sizeofscreen[0] // 2 - button_width // 2, 420, button_width, button_height, "설정 저장", pygame.Color('orange'), pygame.Color('coral'))
button_back = Button(10 , 20, 130, button_height//2+10, "뒤로가기", pygame.Color('navy'), pygame.Color('skyblue'))

button_2560 = Button(sizeofscreen[0] // 2 - button_width // 2, 120, button_width, button_height, "2560x1440", pygame.Color('blue'), pygame.Color('lightblue'))
button_1920 = Button(sizeofscreen[0] // 2 - button_width // 2, 220, button_width, button_height, "1920x1080", pygame.Color('green'), pygame.Color('lightgreen'))
button_1280 = Button(sizeofscreen[0] // 2 - button_width // 2, 320, button_width, button_height, "1280x720", pygame.Color('red'), pygame.Color('salmon'))
button_640 = Button(sizeofscreen[0] // 2 - button_width // 2, 420, button_width, button_height, "640x480", pygame.Color('purple'), pygame.Color('plum'))


button_colormode_on = Button(sizeofscreen[0] // 2 - button_width // 2, 120, button_width, button_height, "색약모드 ON", pygame.Color('blue'), pygame.Color('lightblue'))
button_colormode_off = Button(sizeofscreen[0] // 2 - button_width // 2, 220, button_width, button_height, "색약모드 OFF", pygame.Color('green'), pygame.Color('lightgreen'))

button_reset = Button(sizeofscreen[0] // 2 - button_width // 2, 120, button_width, button_height, "설정 초기화", pygame.Color('purple'), pygame.Color('plum'))

current_screen=1

while True :
    while current_screen == 1 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(pygame.Color('white'))
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_size.rect.collidepoint(event.pos):
                current_screen = 2
                break

            elif button_keysetting.rect.collidepoint(event.pos):
                current_screen = 3
                break

            elif button_colormode.rect.collidepoint(event.pos):
                current_screen = 4
                break

            elif button_settingreset.rect.collidepoint(event.pos):
                current_screen = 5
                break

        if button_size.is_hovered(mouse_pos):
            button_size.color = button_size.hover_color
        else:
            button_size.color = pygame.Color('blue')
        button_size.draw(screen)

        if button_keysetting.is_hovered(mouse_pos):
            button_keysetting.color = button_keysetting.hover_color
        else:
            button_keysetting.color = pygame.Color('green')
        button_keysetting.draw(screen)

        if button_colormode.is_hovered(mouse_pos):
            button_colormode.color = button_colormode.hover_color
        else:
            button_colormode.color = pygame.Color('red')
        button_colormode.draw(screen)

        if button_settingreset.is_hovered(mouse_pos):
            button_settingreset.color = button_settingreset.hover_color
        else:
            button_settingreset.color = pygame.Color('purple')
        button_settingreset.draw(screen)

        if button_save.is_hovered(mouse_pos):
            button_save.color = button_save.hover_color
        else:
            button_save.color = pygame.Color('orange')
        button_save.draw(screen)

        if button_back.is_hovered(mouse_pos):
            button_back.color = button_back.hover_color
        else:
            button_back.color = pygame.Color('navy')
        button_back.draw(screen)

        pygame.display.update()

    while current_screen == 2 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(pygame.Color('white'))
        pygame.display.set_caption('화면 크기 설정')

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_2560.rect.collidepoint(event.pos):
                sizeofscreen = (2560, 1440)
                resize_window(sizeofscreen[0],sizeofscreen[1])
                break

            elif button_1920.rect.collidepoint(event.pos):
                sizeofscreen = (1920, 1080)
                resize_window(sizeofscreen[0],sizeofscreen[1])
                break

            elif button_1280.rect.collidepoint(event.pos):
                sizeofscreen = (1280, 720)
                resize_window(sizeofscreen[0],sizeofscreen[1])
                break

            elif button_640.rect.collidepoint(event.pos):
                sizeofscreen = (640, 480)
                resize_window(sizeofscreen[0], sizeofscreen[1])
                break


        if button_2560.is_hovered(mouse_pos):
            button_2560.color = button_2560.hover_color
        else:
            button_2560.color = pygame.Color('blue')
        button_2560.draw(screen)

        if button_1920.is_hovered(mouse_pos):
            button_1920.color = button_1920.hover_color
        else:
            button_1920.color = pygame.Color('green')
        button_1920.draw(screen)

        if button_1280.is_hovered(mouse_pos):
            button_1280.color = button_1280.hover_color
        else:
            button_1280.color = pygame.Color('red')
        button_1280.draw(screen)

        if button_640.is_hovered(mouse_pos):
            button_640.color = button_640.hover_color
        else:
            button_640.color = pygame.Color('purple')
        button_640.draw(screen)

        if button_back.is_hovered(mouse_pos):
            button_back.color = button_back.hover_color
        else:
            button_back.color = pygame.Color('navy')
        button_back.draw(screen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_back.rect.collidepoint(event.pos):
                current_screen = 1
                pygame.display.set_caption('Settings')
                break
        pygame.display.update()

    while current_screen == 3 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(pygame.Color('white'))
        pygame.display.set_caption('키 설정 변경')

        if button_back.is_hovered(mouse_pos):
            button_back.color = button_back.hover_color
        else:
            button_back.color = pygame.Color('navy')
        button_back.draw(screen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_back.rect.collidepoint(event.pos):
                current_screen = 1
                pygame.display.set_caption('Settings')
                break
        pygame.display.update()

    while current_screen == 4 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(pygame.Color('white'))
        pygame.display.set_caption('색약모드 on/off')

        if button_back.is_hovered(mouse_pos):
            button_back.color = button_back.hover_color
        else:
            button_back.color = pygame.Color('navy')
        button_back.draw(screen)

        if button_colormode_on.is_hovered(mouse_pos):
            button_colormode_on.color = button_colormode_on.hover_color
        else:
            button_colormode_on.color = pygame.Color('blue')
        button_colormode_on.draw(screen)

        if button_colormode_off.is_hovered(mouse_pos):
            button_colormode_off.color = button_colormode_off.hover_color
        else:
            button_colormode_off.color = pygame.Color('green')
        button_colormode_off.draw(screen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_back.rect.collidepoint(event.pos):
                current_screen = 1
                pygame.display.set_caption('Settings')
                break

            if button_colormode_on.rect.collidepoint(event.pos):
                is_colormode=1
                colormode(is_colormode)
                break

            elif button_colormode_off.rect.collidepoint(event.pos):
                is_colormode=0
                colormode(is_colormode)
                break

        pygame.display.update()

    while current_screen == 5 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(pygame.Color('white'))
        pygame.display.set_caption('Settings')

        if button_back.is_hovered(mouse_pos):
            button_back.color = button_back.hover_color
        else:
            button_back.color = pygame.Color('navy')
        button_back.draw(screen)

        if button_reset.is_hovered(mouse_pos):
            button_reset.color = button_reset.hover_color
        else:
            button_reset.color = pygame.Color('purple')
        button_reset.draw(screen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_back.rect.collidepoint(event.pos):
                current_screen = 1
                pygame.display.set_caption('Settings')
                break

            if button_reset.rect.collidepoint(event.pos):
                sizeofscreen = (640, 480)
                resize_window(sizeofscreen[0],sizeofscreen[1])
                colormode(0)
                break

        pygame.display.update()