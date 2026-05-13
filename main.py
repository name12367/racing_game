import math
import re
import time
import pygame

from gasoline import *
from player import Player
from car_bot import *
from white_line import *
from background import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("race")

all_sprites = pygame.sprite.LayeredUpdates()
cars = pygame.sprite.Group()
gasoline_sprites = pygame.sprite.Group()

background_speed = 5
bg1 = Background(y=5, speedy=background_speed)
bg2 = Background(y=-HEIGHT, speedy=background_speed)
clock = pygame.time.Clock()
times = {}
running = True
state = "start"


car_player = Player(RED, (CAR_W, CAR_H), layer=3)
all_sprites.add(car_player)
all_sprites.add(bg1, layer=0)
all_sprites.add(bg2, layer=0)


def delay(time, time_key_name):
    if not time_key_name in times:
        times[str(time_key_name)] = 0

    if math.fabs(pygame.time.get_ticks() - times[time_key_name]) >= time:
        times[time_key_name] = pygame.time.get_ticks()
        return True
    return False

def set_state(_state="start"):
    global state
    state = _state

def save_highest_score(score):
    with open("config.py", "r") as file:
        text = file.read()

    start = text.find("HIGHEST_SCORE =")

    if start != -1:
        end = text.find("\n", start)

        if end == -1:
            end = len(text)

        text = text[:start] + f"HIGHEST_SCORE = {score}" + text[end:]


    with open("config.py", "w") as file:
            file.write(text)

def draw_text(screen, text: str, size: int, color=RED, cord=(0, 0), alignment='left'):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if alignment == "center":
        text_rect.center = cord
    elif alignment == "left":
        text_rect.topleft = cord
    else:
        print("alignment not found")
    screen.blit(text_surface, text_rect)


def restart_the_game():
    global bg1, bg2, times, background_speed
    bg1.rect.y = 5
    bg2.rect.y = -HEIGHT
    background_speed = 5
    times = {}

    for car in cars:
        cars.remove(car)

    car_player.resurrect()
    car_player.restart()
    for sprite in all_sprites:
        sprite.restart()
    for sprite in gasoline_sprites:
        sprite.kill()

# LEVEL 1
def lvl_1():

    if delay(random.choice([1500, 2000, 1750, 1000]), "car_last_spawn_time"):
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


    if delay(500, "line_last_spawn_time"):
        all_sprites.add(WhiteLinePart(WHITE, speedy=background_speed, layer=1))

    if delay(16000, "gas_last_spawn_time"):
        gasoline_sprites.add(Gasoline(speedy=5, layer=4))

        # Check collisions
    car_hits = pygame.sprite.spritecollide(car_player, cars, False)
    gas_hits = pygame.sprite.spritecollide(car_player, gasoline_sprites, True)
    if gas_hits:
        car_player.refill()

    if car_hits:
        if delay(2000, "player_collision_time"):
            car_player.unset_collided()

        if not car_player.is_collided():
            car_player.decrease_lives()
            car_player.set_collided()

    if car_player.is_dead():
        set_state("game_over")

    all_sprites.update()
    cars.update()
    gasoline_sprites.update()

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
    gasoline_sprites.draw(screen)
    draw_text(screen, f"{car_player.lives} lives", 34, RED, (15, 15), alignment="left")
    fuel = round(car_player.fuel, 1)
    draw_text(screen, f"Fuel: {fuel}", 34, ORANGE, (15, 55), alignment="left")
    if car_player.score > HIGHEST_SCORE:
        score_color = GOLD
    else:
        score_color = SILVER

    draw_text(screen, f"score: {car_player.score}", 46, score_color, (WIDTH / 2, 40), alignment="center")
    pygame.display.update()

# game over screen
def game_over_screen():
    screen.fill((RED))
    draw_text(screen, "game over!", 40, WHITE, (WIDTH / 2, HEIGHT / 2 - 70), alignment="center")
    draw_text(screen, "press space to start again", 40, WHITE, (WIDTH / 2, HEIGHT / 2 - 20), alignment="center")
    if car_player.score > HIGHEST_SCORE:
        draw_text(screen, f"NEW highest score: {car_player.score}", 40, GOLD, (WIDTH / 2, HEIGHT / 2 + 30),alignment="center")
    else:
        draw_text(screen, f"highest score: {HIGHEST_SCORE}", 40, SILVER, (WIDTH / 2, HEIGHT / 2 + 30), alignment="center")
    pygame.display.update()

# START SCREEN
def start_screen():
    screen.fill(BLACK)
    draw_text(screen, "press space to race", 40, WHITE, (WIDTH / 2, HEIGHT / 2 - 50), alignment="center")
    pygame.display.update()

while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == "game_over":
                    restart_the_game()
                state = 'level_1'
            if event.key == pygame.K_r:
                restart_the_game()
            if event.key == pygame.K_ESCAPE:
                state = 'start'
                restart_the_game()


    # Calculations
    if state == 'start':
        start_screen()
    elif state == 'level_1':
        lvl_1()
    elif state == "game_over":
        if HIGHEST_SCORE < car_player.score:
            save_highest_score(car_player.score)
        game_over_screen()


    clock.tick(60)

pygame.quit()