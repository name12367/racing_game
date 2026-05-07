import pygame
import math
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
        self.dead = False
        self.player_collision_time = 0

    def delay_is_out(self):
        return math.fabs(pygame.time.get_ticks() - self.player_collision_time) >= 3000

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
        if self.lives == 0:
            self.dead = True

    def set_collided(self):
        self.collided = True

    def resurrect(self):
        self.dead = False

    def unset_collided(self):
        self.collided = False

    def is_collided(self):
        return self.collided

    def is_dead(self):
        return self.dead

    def restart(self):
        self.speedx = 0
        self.lives = PLAYER_LIVES
        self.player_collision_time = 0

    def set_collision_time(self, time):
        self.player_collision_time = time