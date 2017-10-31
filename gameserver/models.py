#!/usr/bin/env python3
import ujson
import os
import logging
import time

field = [[0 for i in range(30)] for j in range(30)]


class GameObjectFactory:
    """Factory for game objects.
    """

    def __init__(self, directory="objects"):
        self._objects = {
        }

        for f in os.listdir(directory):
            if f.endswith('json'):
                logging.info(f"Loading object description file: {f}")
                try:
                    path = os.path.join(directory, f)
                    objects = ujson.load(open(path, "r"))
                    for name, obj in objects.items():
                        self.register(obj, name)
                except Exception as exc:
                    logging.warning(f"Error loading {f}:\n\t{exc}")

    def register(self, obj, name):
        """Register unit configuration.
        """
        self._objects[name] = obj


factory = GameObjectFactory()


class GameLoop:
    def __init__(self, field, tps=32):
        self.tick_number = 0
        self.tps = tps
        self.interval = 1 / tps
        self._shedule = {}

    def shedule():
        pass

    def tick():
        pass

    def push():
        pass

    def start_main_loop(self):
        while True:
            self.tick_number += 1
            tick_start_time = time.time()
            print(f"Tick started at {tick_start_time}")

            self.tick()
            self.push()

            delta = tick_start_time - time.time()

            if delta < self.interval:
                time.sleep(self.interval - delta)


# GameLoop(field).start_main_loop()

class Cell:
    """Field cell objects.
    """

    def __init__(self, x, y, content, up, down, left, right):
        self.x = x
        self.y = y
        self.content = content
        self.up = up
        self.down = down
        self.left = left
        self.right = right


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


class Healer(GameObject):
    """Class for healing Ground objects.

    Attributes:
        power (int): Amount of healing a Healer gives per Tick
    """

    def __init__(self, power):
        super().__init__(True, 0)
        self.power = power

    def heal(self, unit):
        if (unit.health) < (unit.max_health):
            if (unit.health + self.power <= unit.max_health):
                unit.health += self.power
            else:
                unit.health = unit.max_health


class Loader(GameObject):
    """Class for loading Ground objects.

    Attributes:
        power (int): Amount of bullets a Loader gives per Tick
        bullet (Bullet) Type of bullets a Loader gives
    """

    def __init__(self, power, bullet):
        super().__init__(True, 0)
        self.power = power
        self.bullet = bullet

    def load(self, unit):
        if (unit.magazine) < (unit.max_magazine):
            if unit.bullet != self.bullet:
                unit.magazine = 0
                unit.bullet = bullet
            if (unit.magazine + self.power <= unit.max_magazine):
                unit.magazine += self.power
            else:
                unit.magazine = unit.max_magazine


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
