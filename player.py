import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, fill_color=WHITE, size=(CAR_H, CAR_W), layer=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(fill_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.layer = layer
        self.lives = PLAYER_LIVES
        self.collided = False

    def update(self):
        self.speedx = 0

        keystate = pygame.key.get_pressed()
        if self.rect.x >= WIDTH - CAR_W - 5:
            self.rect.x -= 5
        if self.rect.x <= 5:
            self.rect.x += 5
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        self.rect.x += self.speedx

    def decrease_lives(self):
        if self.lives >= 1:
            self.lives -= 1

    def set_collided(self):
        self.collided = True

    def unset_collided(self):
        self.collided = False

    def is_collided(self):
        return self.collided