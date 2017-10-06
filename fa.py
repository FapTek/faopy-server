import ujson

field = [[0 for i in range(30)] for j in range(30)]


class Square:  # field square objects
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content


class GameObject:  # basic objects
    def __init__(self, stackable, speed):
        self.stackable = stackable
        self.speed = speed

# place for content class


class Bullet(GameObject):  # bullet objects
    def __init__(self, stackable, speed, damage):
        super().__init__(True, speed)
        self.damage = damage


class Unit(GameObject):  # objects of Players and all kinds of mobs
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
    # NB LET'S FIGURE THAT OUT AS SOON AS POSSIBLE, IT IS TRAGICALLY AWFULL
    dictionary = data[name]
    unit = Unit(dictionary['bullet'],  dictionary['direction'], dictionary['health'], dictionary['magazine'],
                dictionary['max_health'], dictionary['max_magazine'], dictionary['melee_damage'], dictionary['speed'], dictionary['x'], dictionary['y'])
    return unit
