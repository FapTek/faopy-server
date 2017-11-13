#!/usr/bin/env python2
import models
import time
import logging


class World:
    def __init__(self, viewstate, tps=32):
        self.tick_number = 0
        self.tps = tps
        self.interval = 1 / tps
        self._shedule = {}
        self.field = models.Field()

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
