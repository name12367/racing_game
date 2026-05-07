import math
import time
import pygame

from player import Player
from car_bot import *
from white_line import *
from background import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("race")

all_sprites = pygame.sprite.LayeredUpdates()
cars = pygame.sprite.Group()

background_speed = 5
bg1 = Background(y=5, speedy=background_speed)
bg2 = Background(y=-HEIGHT, speedy=background_speed)
car_player = Player(RED, (CAR_W, CAR_H), layer=3)

all_sprites.add(car_player)
all_sprites.add(bg1, layer=0)
all_sprites.add(bg2, layer=0)

clock = pygame.time.Clock()
times = {"one": 1, "two": 2}
car_last_spawn_time = 0
line_last_spawn_time = 0
player_collision_time = 0
running = True
state = "start_screen"

def save_key(time_value, time_key_name):
    times[time_key_name] = time_value

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def restart_the_game():
    global bg1, bg2, car_last_spawn_time, line_last_spawn_time, background_speed
    bg1.rect.y = 5
    bg2.rect.y = -HEIGHT
    background_speed = 5
    line_last_spawn_time = 0

    car_last_spawn_time = 0
    for car in cars:
        cars.remove(car)

    car_player.resurrect()
    car_player.restart()
    for i in all_sprites:
        i.restart()

# LEVEL 1
def lvl_1():
    global car_last_spawn_time, line_last_spawn_time
    if math.fabs(pygame.time.get_ticks() - car_last_spawn_time) >= random.choice([1500, 2000, 1750, 1000]):
        cars.add(
            CarBot(
                random.choice([YELLOW, GREEN]),
                random.randint(
                    background_speed - 3,
                    background_speed - 1
                ),
                layer=2
            )
        )
        car_last_spawn_time = pygame.time.get_ticks()

    if math.fabs(pygame.time.get_ticks() - line_last_spawn_time) >= 500:
        line_last_spawn_time = pygame.time.get_ticks()
        all_sprites.add(WhiteLinePart(WHITE, speedy=background_speed, layer=1))

        # Check collisions
    hits = pygame.sprite.spritecollide(car_player, cars, False)
    time_delay = math.fabs(pygame.time.get_ticks() - car_player.player_collision_time) >= 3000
    if hits:
        if time_delay:
            car_player.unset_collided()

        if not car_player.is_collided():
            car_player.set_collision_time(pygame.time.get_ticks())
            car_player.decrease_lives()

            if car_player.is_dead():
                restart_the_game()

            car_player.set_collided()


    all_sprites.update()
    cars.update()

    if bg1.is_in_centre():
        bg2.rect.y = -HEIGHT

    if bg2.is_in_centre():
        bg1.rect.y = -HEIGHT

    for car in cars:
        if car.is_on_the_edge():
            cars.remove(car)

    # Rendering
    screen.fill(BLACK)
    all_sprites.draw(screen)
    cars.draw(screen)
    draw_text(screen, f"{car_player.lives} lives", 50, RED, 20, 20)
    pygame.display.update()

# START SCREEN
def start_screen():
    screen.fill(BLACK)
    draw_text(screen, "press space to race", 40, WHITE, 75, 200)
    pygame.display.update()

while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = 'level_1'
            if event.key == pygame.K_r:
                restart_the_game()
            if event.key == pygame.K_ESCAPE:
                state = 'start_screen'
    # Calculations
    if state == 'start_screen':
        start_screen()
    elif state == 'level_1':
        lvl_1()

    clock.tick(60)

pygame.quit()