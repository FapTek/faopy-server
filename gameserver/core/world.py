#!/usr/bin/env python2
from core import objects
import time
import os
import enum


class World:
    def __init__(self, viewstate, tps=32):
        self.tick_number = 0
        self.tps = tps
        self.interval = 1 / tps
        self._shedule = {}
        self.field = Field()

    def shedule(self):
        pass

    def tick(self):
        for obj in self.field.objects:
            obj.tick()

    def push(self):
        pass

    def start_main_loop(self):
        while True:
            self.tick_number += 1
            tick_start_time = time.time()

            self.tick()
            self.push()
            self.field._debug()

            delta = tick_start_time - time.time()

            if delta > self.interval:
                print(f"Can't keep up, skipping tick #{self.tick_number}")
            elif delta < self.interval:
                time.sleep(self.interval - delta)


class Field:
    """Represents game field
    """
    def __init__(self, size=10):
        self._field = [
            [Cell(self, i, j) for j in range(size)] for i in range(size)
        ]
        self.objects = []
        # self.add(objects.TestAI())
        self.size = size

    def add(self, obj, x=0, y=0):
        if self._field[x][y].busy:
            # TODO find a place for the object maybe?
            return
        obj.locate(self._field[x][y])
        self._field[x][y].content.append(obj)
        self.objects.append(obj)

    def _debug(self):
        pass
        # os.system("clear")
        # for i in self._field:
        #     for j in i:
        #         if j.empty:
        #             print(" ", end="")
        #         else:
        #             print(".", end="")
        #     print()


class Cell:
    """Field cell objects.
    """

    def __init__(self, field, x, y, content=None, borders=None):
        self.field = field
        self.x = x
        self.y = y
        self.content = content or list()
        self.borders = borders or list()

    def clear(self):
        self.content = []

    def neighbour(self, direction):
        x = self.x + direction.x
        y = self.y + direction.y
        if max(x, y) < self.field.size and min(x, y) >= 0:
            return self.field._field[x][y]

    @property
    def busy(self):
        for obj in self.content:
            if not obj.stackable:
                return True
        return False

    @property
    def empty(self):
        return len(self.content) == 0


class Direction(enum.Enum):
    """Represents Direction
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Direction(tuple(map(lambda x: -x, self.value)))
