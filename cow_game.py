from dataclasses import dataclass
from designer import *
from random import randint
import time


@dataclass
class World:
    sky: DesignerObject
    cow: DesignerObject
    grass: DesignerObject
    apples: list[DesignerObject]
    cow_speed: int
    platforms: list[DesignerObject]
    end_text: DesignerObject
    APPLE_FALLING_SPEED: int
    start_time: time


def create_sky() -> DesignerObject:
    """ Create the sky """
    sky = rectangle("#9cedff", 10000, 10000)
    sky.y = 515
    sky.flip_x = True
    return sky


def create_grass() -> DesignerObject:
    """ Create the grass """
    grass = rectangle("green", 2000, 200)
    grass.y = 515
    grass.flip_x = True
    return grass


def create_cow() -> DesignerObject:
    """ Create the cow """
    cow = emoji("cow")
    cow.y = 400
    cow.flip_x = True
    return cow


def create_world() -> World:
    """ Create the world """
    return World(create_sky(), create_cow(), create_grass(), [], 25, [], text("black", "0", 50, get_width() / 2, 40),
                 10, time.time())


def head_left(world: World):
    """ Make the cow start moving left """
    world.cow_speed = abs(world.cow_speed)
    world.cow.flip_x = False
    world.cow.x -= world.cow_speed


def head_right(world: World):
    """ Make the cow start moving right """
    world.cow_speed = abs(world.cow_speed)
    world.cow.flip_x = True
    world.cow.x += world.cow_speed


def bounce_cow(world: World):
    """ Handle the cow bouncing off a wall """
    if world.cow.x > get_width():
        head_left(world)
    elif world.cow.x < 0:
        head_right(world)


def flip_cow(world: World, key: str):
    """ Change the direction that the cow is moving """
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)


def create_apple() -> DesignerObject:
    """ Create a small apple randomly on the top of the screen """
    apple = emoji('🍎')
    apple.scale_x = 1
    apple.scale_y = 1
    apple.anchor = 'midtop'
    apple.x = randint(0, get_width())
    apple.y = 0
    return apple


def create_new_apple(world: World):
    """ Create a new apple randomly"""
    if len(world.apples) < 30 and randint(1, 50) == 25:
        new_apple = create_apple()
        world.apples.append(new_apple)


def cow_eats_apples(world: World):
    eaten_apples = []
    destroyed_apples = []
    for apple in world.apples:
        if colliding(apple, world.cow):
            world.cow.scale_x += 1
            world.cow.scale_y += 1
            eaten_apples.append(apple)
            destroyed_apples.append(apple)
            world.cow.y -= 15
    for apple in eaten_apples:
        world.apples.remove(apple)
        destroy(apple)


def apples_falling(world: World):
    """ Make the apples fall """
    for falling_apple in world.apples:
        falling_apple.y += world.APPLE_FALLING_SPEED


def cow_is_big(world: World) -> bool:
    """ detects when the cow reaches the right size """
    return world.cow.scale_x >= 10


def update_timer(world):
    """ Update the timer """
    end_time = time.time()
    elapsed_time = (end_time - world.start_time) // 1
    world.end_text.text = "time passed: " + str(elapsed_time)


def game_over_win(world):
    """end the game when the cow eats enough apples and gets big enough"""
    end_time = time.time()
    world.end_text.text = "Game Over! Your time was " + str((end_time - world.start_time) // 1)


when("updating", apples_falling)
when("updating", update_timer)
when("updating", create_new_apple)
when(cow_is_big, game_over_win, pause)
when("updating", cow_eats_apples)
when("typing", flip_cow)
when('starting', create_world)
when("updating", bounce_cow)
start()

