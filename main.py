import math
import time

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
        car_spawn_times = random.choice([1500, 2000, 1750, 1000])

    if math.fabs(pygame.time.get_ticks() - line_last_spawn_time) >= 500:
        line_last_spawn_time = pygame.time.get_ticks()
        all_sprites.add(WhiteLinePart(WHITE, speedy=background_speed, layer=1))

    # Check collisions
    hits = pygame.sprite.spritecollide(car_player, cars, False)
    if hits:
        if not car_player.is_collided():
            car_player.decrease_lives()
            car_player.set_collided()
            print(car_player.lives) # nen

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
    pygame.display.flip()

    clock.tick(60)

pygame.quit()