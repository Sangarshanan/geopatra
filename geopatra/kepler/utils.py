import random
import string


def random_char(y):
    return "".join(random.choice(string.ascii_letters) for x in range(y))
