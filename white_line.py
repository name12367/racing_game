import pygame
from config import *

class WhiteLinePart(pygame.sprite.Sprite):
    def __init__(self, color=WHITE, speedy=5, layer=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 100))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0
        self.speedy = speedy
        self.layer = layer

    def update(self):
        self.rect.y += self.speedy

    def is_on_the_edge(self):
        if HEIGHT <= self.rect.top:
            return True
        return False