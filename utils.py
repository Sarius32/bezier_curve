from random import randint

def random_color() -> str:
    return "#%02x%02x%02x" % (randint(0, 255), randint(0, 255), randint(0, 255))