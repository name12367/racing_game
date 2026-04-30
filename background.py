import pygame
from config import *


class Background(pygame.sprite.Sprite):
    def __init__(self, layer=0, speedy=5, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images/bg.png").convert(), (WIDTH, HEIGHT + 5))
        self.rect = self.image.get_rect()
        self.layer = layer
        self.speedy = speedy
        self.rect.y = y

    def update(self):
        self.rect.y += self.speedy

    def is_in_centre(self):
        if HEIGHT + 5 <= self.rect.bottom and self.rect.bottom <= HEIGHT + 5:
            return True
        return False

    def restart(self):
        pass