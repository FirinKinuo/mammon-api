import random
from string import ascii_lowercase, digits


def random_string(length: int) -> str:
    """
    Generates a string of random characters of the given length
    Args:
        length (int): Generated string length

    Returns:
        str: Generated string
    """
    return ''.join(random.choice(ascii_lowercase) for _ in range(length))


def random_int(length: int) -> int:
    """
    Generates a random integer digit of the given length
    Args:
        length (int): Длина генерируемой цифры

    Returns:
        str: Generated int
    """
    return int(''.join(random.choice(digits) for _ in range(length)))
