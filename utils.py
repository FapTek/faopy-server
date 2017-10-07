import logging
import traceback

def t(t):
    def type_decorator(func):
        def wrapped(self, arg):
            if type(arg) == t:
                return func(self, arg)
            else:
                logging.warning(f"Type mismatch in call to {func.__name__}: expected {t}, got {type(arg)}")
        return wrapped
    return type_decorator
