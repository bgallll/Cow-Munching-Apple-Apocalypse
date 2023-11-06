from dataclasses import dataclass
from designer import *
from random import randint

# Set speed of the copter
COW_SPEED = 15


@dataclass
class World:
    sky: DesignerObject
    cow: DesignerObject
    grass: DesignerObject
    cow_speed: int
    platforms: list[DesignerObject]
    timer: int


def create_sky() -> DesignerObject:
    """ Create the sky """
    sky = rectangle("#9cedff", 10000, 10000)
    sky.y = 515
    sky.flip_x = True
    return sky


def create_cow() -> DesignerObject:
    """ Create the cow """
    cow = emoji("cow")
    cow.y = 400
    cow.flip_x = True
    return cow


def create_grass() -> DesignerObject:
    """ Create the grass """
    grass = rectangle("green", 2000, 200)
    grass.y = 515
    grass.flip_x = True
    return grass


def create_world() -> World:
    """ Create the world """
    return World(create_sky(), create_cow(), create_grass(), COW_SPEED, 0, 0)


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


when("typing", flip_cow)
when('starting', create_world)
when("updating", bounce_cow)
start()
