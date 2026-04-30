import pygame
import random
from config import *

class CarBot(pygame.sprite.Sprite):
    car_spawn_coords = (20, 75, 130, 220, 275, 330)

    def __init__(self, color=WHITE, speedy=5, layer=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 100))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(self.car_spawn_coords)
        self.rect.y = 0 - CAR_H
        self.speedx = 0
        self.speedy = speedy
        self.layer = layer
        self.lives = PLAYER_LIVES
        self.last_spawn_time = 0

    def update(self):
        self.rect.y += self.speedy

    def is_on_the_edge(self):
        if CAR_H + HEIGHT <= self.rect.y:
            return True
        return False

    def restart(self):
        self.speedy = 5
