#!/usr/bin/env python3
from core import world


class GameObject:
    """Base class for all objects on the field.

    Attributes:
        stackable (bool): No more than one unstackable object can be in a cell.
        speed (int): Amount of ticks needed for object to move. Immovable
            objects have a `speed` of zero.
     """

    def __init__(self,
                 stackable=True,
                 speed=0):
        self.stackable = stackable
        self.speed = speed
        self.cell = None

    def locate(self, cell):
        self.cell = cell

    def tick(self):
        pass

    @property
    def orphan(self):
        return self.cell is None

    def move(self, direction):
        if not self.orphan:
            if direction not in self.cell.borders:
                target = self.cell.neighbour(direction)
                if target:
                    self.cell.content.remove(self)
                    self.locate(target)
                    target.content.append(self)
                    return True
        return False


class Healer(GameObject):
    """Class for healing Ground objects.

    Attributes:
        power (int): Amount of healing a Healer gives per Tick
    """

    def __init__(self, power):
        super().__init__()
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
        super().__init__()
        self.power = power
        self.bullet = bullet

    def load(self, unit):
        if (unit.magazine) < (unit.max_magazine):
            if unit.bullet != self.bullet:
                unit.magazine = 0
                unit.bullet = self.bullet
            if (unit.magazine + self.power <= unit.max_magazine):
                unit.magazine += self.power
            else:
                unit.magazine = unit.max_magazine


class Weapon:
    def __init__(self, damage, speed):
        self.damage = damage
        self.speed = speed


class Bullet(GameObject):
    """Base class for bullets.

    Attributes:
        damage (int): Amount of damage a bullet causes
    """

    def __init__(self,
                 damage=250,
                 speed=4):
        super().__init__(speed=speed)
        self.type = Weapon(damage, speed)


class Unit(GameObject):
    """Base class for players and mobs

    Attributes:
        direction (str): The direction a unit is facing.
        health (int): Unit HP.
        max_health (int): Maximum health of a unit. A unit can't be healed over
            it, but can spawn with `health` more than `max_health`.
        bullet_type (str): Weapon type a unit uses.
        magazine (int): Amount of available bullets.
        max_magazine (int): Maximum amount of bullets of a unit. A unit can't
            pick more bullets, but can spawn with `magazine` > `max_magazine`.
        melee_damage (int): Amount of damage caused upon colliding with other
            unit.
    """

    def __init__(self, bullet,  direction, health, magazine, max_health,  max_magazine,  melee_damage, speed):
        super().__init__(speed=speed)
        self.direction = direction
        self.max_health = max_health
        self.health = health
        self.bullet = bullet
        self.magazine = magazine
        self.max_magazine = max_magazine
        self.melee_damage = melee_damage


class TestAI(Unit):
    def __init__(self):
        super().__init__(Bullet(),
                         world.Direction.UP,
                         10,
                         10,
                         100,
                         100,
                         100,
                         10)

    def tick(self):
        if not self.move(self.direction):
            self.direction = - self.direction
