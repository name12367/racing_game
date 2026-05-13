import random
import pygame
from config import *

class Gasoline(pygame.sprite.Sprite):
    gas_spawn_cords = (45, 100, 155, 245, 300, 355)
    def __init__(self, speedy=5, layer=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images/gasoline.png").convert_alpha(), (75, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(self.gas_spawn_cords)
        self.rect.bottom = 0
        self.speedy = speedy
        self.layer = layer

    def update(self):
        self.rect.y += self.speedy

    def is_on_the_edge(self):
        if HEIGHT <= self.rect.top:
            return True
        return False

    def restart(self):
        self.speedy = 5
        self.rect.bottom = 0