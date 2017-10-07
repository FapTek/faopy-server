import ujson

field = [[0 for i in range(30)] for j in range(30)]


class Square:  # field square objects
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


def factory(name):  # some function to create units
    data = ujson.load(open("fa.json", "r"))
    dictionary = data[name]
    unit = Unit(**dictionary)
    return unit
