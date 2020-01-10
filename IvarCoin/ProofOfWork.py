import hashlib
import random
import string
from datetime import datetime
import base64

min_bits = 0
max_bits = 160


def is_valid(result):
    return validate(result, int(result.split(':')[1]))


def validate(string_, bite):
    if bite > max_bits or bite <= 0:
        raise ValueError("0-160 bites, {} was given".format(bite))
    i = 0
    total = 0
    N = int(bite / 8)
    string_ = string_.encode("utf-8")
    x = hashlib.sha1(string_).digest()

    while i < N:
        total |= x[i]
        i += 1

    remainder = bite % 8
    if remainder != 0:
        total |= x[i] >> (8 - remainder)

    return total == 0


def generate(data, bite):
    ver = "1"
    bite = bite
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M")
    ext = ""
    letters = string.ascii_letters
    rand = "".join(random.choice(letters) for i in range(10))
    counter = 0

    while True:
        string_ = ":".join(str(elm) for elm in [ver, bite, date_time, data, ext, rand, counter])
        if validate(string_, bite):
            result = string_
            break
        counter += 1
    return result


