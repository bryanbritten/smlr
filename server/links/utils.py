import random

# exclude characters that are easy to confuse, like 0 and O
CHARS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
MIN_VAL = 1000000000


def generate_id() -> int:
    # define this as a function in case the approach changes in the future
    value = random.getrandbits(64)
    if value < MIN_VAL:
        value += MIN_VAL

    return value


def encode(num) -> str:
    remainder = num % len(CHARS)
    encoded_string = CHARS[remainder]
    quotient = num // len(CHARS)
    while quotient:
        remainder = quotient % len(CHARS)
        quotient = quotient // len(CHARS)
        encoded_string = CHARS[remainder] + encoded_string

    return encoded_string


def decode(encoded_string: str) -> int:
    record_id = 0

    for i, char in enumerate(encoded_string):
        record_id += CHARS.find(char) * (len(CHARS) ** (len(encoded_string) - i - 1))

    return record_id
