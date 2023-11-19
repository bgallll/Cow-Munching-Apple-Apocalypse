from dataclasses import dataclass
from designer import *
from random import randint

# Set speed of the copter
COW_SPEED = 25
APPLE_FALLING_SPEED = 10


@dataclass
class World:
    sky: DesignerObject
    cow: DesignerObject
    grass: DesignerObject
    apples: list[DesignerObject]
    cow_speed: int
    platforms: list[DesignerObject]
    timer: int


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
    return World(create_sky(), create_cow(), create_grass(), [], COW_SPEED, 0, [])


def head_left(world: World):
    """ Make the cow start moving left """
    world.cow_speed = -COW_SPEED
    world.cow.flip_x = False
    world.cow.x += (world.cow_speed)


def head_right(world: World):
    """ Make the cow start moving right """
    world.cow_speed = COW_SPEED
    world.cow.flip_x = True
    world.cow.x += COW_SPEED


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
    if len(world.apples) < 10 and randint(1, 50) == 25:
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
        falling_apple.y += APPLE_FALLING_SPEED


when("updating", apples_falling)
when("updating", create_new_apple)
when("updating", cow_eats_apples)
when("typing", flip_cow)
when('starting', create_world)
when("updating", bounce_cow)
start()
