#!/usr/bin/env python3
import os
import logging
import ujson


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
