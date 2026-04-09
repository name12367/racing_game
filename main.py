import math
import random
from random import choice

from player import Player
from car_bot import *
from white_line import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("race")

all_sprites = pygame.sprite.LayeredUpdates()
cars = pygame.sprite.Group()
car_player = Player(RED, (CAR_W, CAR_H), layer=2)
all_sprites.add(car_player)


clock = pygame.time.Clock()
car_last_spawn_time = 0
line_last_spawn_time = 0
car_spawn_times = random.choice((1500, 2000, 2500, 1000))
running = True
while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculations
    if math.fabs(pygame.time.get_ticks() - car_last_spawn_time) >= car_spawn_times:
        cars.add(CarBot(random.choice([RED, GREEN]), random.randint(4, 7), layer=1))
        cars.add(CarBot(random.choice([RED, GREEN]), random.randint(4, 7), layer=1))
        cars.add(CarBot(random.choice([RED, GREEN]), random.randint(4, 7), layer=1))
        cars.add(CarBot(random.choice([RED, GREEN]), random.randint(4, 7), layer=1))
        car_last_spawn_time = pygame.time.get_ticks()
        car_spawn_times = random.choice([1500, 2000, 1750, 1000])

    if math.fabs(pygame.time.get_ticks() - line_last_spawn_time) >= 500:
        line_last_spawn_time = pygame.time.get_ticks()
        all_sprites.add(WhiteLinePart(WHITE, 5, layer=0))

    all_sprites.update()
    cars.update()

    for car in cars:
        if car.is_on_the_edge():
            cars.remove(car)

    # Rendering
    screen.fill(BLACK)
    all_sprites.draw(screen)
    cars.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()