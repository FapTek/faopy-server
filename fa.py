#!/usr/bin/p
import ujson
import os
import logging
from utils import t

field = [[0 for i in range(30)] for j in range(30)]

class GameObjectFactory:
    """Factory for game objects.
    """
    def __init__(self, directory="objects"):
        self._objects = {}

        for subdir, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith('json'):
                    logging.info(f"Loading object description: {f}")
                    try:
                        path = os.path.join(subdir, f)
                        obj = ujson.load(open(path, "r"))
                        self.register(obj)
                    except Exception as exc:
                        logging.warning(f"Error loading {f}:\n\t{exc}")

    def register(self, obj):
        """Register unit configuration.
        """
        pass

factory = GameObjectFactory()


class Cell:
    """Field cell objects.
    """
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content


class GameObject:
    """Base class for all objects on the field.

    Attributes:
        stackable (bool): No more than one `stackable` object can be in a field cell.
        speed (int): Amount of ticks needed for object to move. Immovable objects
            have a `speed` of zero.
     """
    def __init__(self,
                 stackable=True,
                 speed=0):
        self.stackable = stackable
        self.speed = speed


# place for content class


class Bullet(GameObject):
    """Base class for bullets.

    Attributes:
        damage (int): Amount of damage a bullet causes
    """
    def __init__(self,
                 damage=250,
                 speed=4):
        super().__init__(speed=speed)
        self.damage = damage


class Unit(GameObject):
    """Base class for players and mobs

    Attributes:
        direction (str): The direction a unit is facing.
        health (int): Unit HP.
        max_health (int): Maximum health of a unit. A unit can't be healed over it,
            but can spawn with `health` more than `max_health`.
        bullet_type (str): Weapon type a unit uses.
        magazine (int): Amount of available bullets.
        max_magazine (int): Maximum amount of bullets of a unit. A unit can't pick up
            more bullets, but can spawn game with `magazine` > `max_magazine`.
        melee_damage (int): Amount of damage caused upon colliding with other unit.
        x (int): x coordinate
        y (int): y coordinate
    """
    def __init__(self, bullet,  direction, health, magazine, max_health,  max_magazine,  melee_damage, speed, x, y):
        super().__init__(False, speed)
        self.direction = direction
        self.max_health = max_health
        self.health = health
        self.bullet = bullet
        self.magazine = magazine
        self.max_magazine = max_magazine
        self.melee_damage = melee_damage
        self.x = x
        self.y = y
