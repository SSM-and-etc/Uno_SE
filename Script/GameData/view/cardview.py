import pygame 
class CardView:
    def __init__(self, card_type, color, x, y):
        self.card_type = card_type
        self.color = color
        self.x = x
        self.y = y
        self.width = 100
        self.height = 140
        self.face_down = True
        
        self.image = pygame.image.load(f'/Material/card/{self.color}/{self.card_type}.jpg')
        self.image_back = pygame.image.load('/Material/card/CARD_BACK.jpg')
        
    def draw(self, surface):
        if self.face_down:
            surface.blit(self.image_back, (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))
