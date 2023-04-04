import pygame

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class CircleButton:
    def __init__(self, x, y, radius, color, hover_color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def is_hover(self, mouse_pos):
        distance = ((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) ** 0.5
        return distance <= self.radius

    def draw(self, surface):
        if self.is_hovered:
            pygame.draw.circle(surface, self.hover_color, (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

class Button:
    def __init__(self, rect, color, text, text_color):
        self.rect = rect
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.SysFont('AppleGothic', 24)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_line_between_buttons(surface, color, start_pos, end_pos):
    pygame.draw.line(surface, color, start_pos, end_pos, 3)

def main():
    pygame.init()

    screen_width, screen_height = 1280, 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("map")

    map_image = pygame.image.load("map.png")

    buttons = []

    button1_pos = (635, 135)
    button2_pos = (1090, 215)
    button3_pos = (400, 530)
    button4_pos = (635, 330)

    button1 = CircleButton(button1_pos[0], button1_pos[1], 10, white, green)
    button2 = CircleButton(button2_pos[0], button2_pos[1], 10, white, red)
    button3 = CircleButton(button3_pos[0], button3_pos[1], 10, white, red)
    button4 = CircleButton(button4_pos[0], button4_pos[1], 10, white, red)

    buttons.append(button1)
    buttons.append(button2)
    buttons.append(button3)
    buttons.append(button4)

    current_button = 0
    buttons[current_button].color = blue


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                button1.is_hovered = button1.is_hover(mouse_pos)
                button2.is_hovered = button2.is_hover(mouse_pos)
                button3.is_hovered = button3.is_hover(mouse_pos)
                button4.is_hovered = button4.is_hover(mouse_pos)

            screen.blit(map_image, (0, 0))
            button1.draw(screen)
            button2.draw(screen)
            button3.draw(screen)
            button4.draw(screen)

            draw_line_between_buttons(screen, red, button1_pos, button2_pos)
            draw_line_between_buttons(screen, red, button2_pos, button3_pos)
            draw_line_between_buttons(screen, red, button3_pos, button4_pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    buttons[current_button].color = white
                    current_button = current_button - 1
                    if current_button < 0 :
                        current_button = 0
                    buttons[current_button].color = blue

                elif event.key == pygame.K_RIGHT:
                    buttons[current_button].color = white
                    current_button = current_button + 1
                    if current_button > 3 :
                        current_button = 3
                    buttons[current_button].color = blue

                elif event.key == pygame.K_RETURN:
                    if current_button == 0 :
                        popup_width, popup_height = 800, 480
                        popup_x, popup_y = 220,160
                        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                        pygame.draw.rect(screen, white, popup_rect)

                        font = pygame.font.SysFont("AppleGothic", 24)
                        text = font.render('현재 지역은 유럽 입니다. 게임에 참가하시겠습니까?', True, (0, 0, 0))
                        text_rect = text.get_rect(center=(popup_x + popup_width / 2, popup_y + popup_height / 2 - 100))
                        screen.blit(text, text_rect)

                    elif current_button == 1 :
                        popup_width, popup_height = 800, 480
                        popup_x, popup_y = 220,160
                        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                        pygame.draw.rect(screen, white, popup_rect)
                        font = pygame.font.SysFont("AppleGothic", 24)
                        text = font.render('현재 지역은 한국 입니다. 게임에 참가하시겠습니까?', True, (0, 0, 0))
                        text_rect = text.get_rect(center=(popup_x + popup_width / 2, popup_y + popup_height / 2 - 100))
                        screen.blit(text, text_rect)

                    elif current_button == 2 :
                        popup_width, popup_height = 800, 480
                        popup_x, popup_y = 220,160
                        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                        pygame.draw.rect(screen, white, popup_rect)
                        font = pygame.font.SysFont("AppleGothic", 24)
                        text = font.render('현재 지역은 남미 입니다. 게임에 참가하시겠습니까?', True, (0, 0, 0))
                        text_rect = text.get_rect(center=(popup_x + popup_width / 2, popup_y + popup_height / 2 - 100))
                        screen.blit(text, text_rect)

                    elif current_button == 3 :
                        popup_width, popup_height = 800, 480
                        popup_x, popup_y = 220, 160
                        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                        pygame.draw.rect(screen, white, popup_rect)
                        font = pygame.font.SysFont("AppleGothic", 24)
                        text = font.render('현재 지역은 아프리카 입니다. 게임에 참가하시겠습니까?', True, (0, 0, 0))
                        text_rect = text.get_rect(center=(popup_x + popup_width / 2, popup_y + popup_height / 2 - 100))
                        screen.blit(text, text_rect)


        pygame.display.update()

if __name__ == '__main__':
    main()