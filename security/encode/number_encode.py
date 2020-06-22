import string


d = {}  # Dictionary to cache the value generated in the next function


# Encode number to base64
def b64encode(number: int):
    """
    Encode a number to base64
    :param number: number
    :return: encoded number
    """
    b = ""
    global d

    if len(d) < 64:
        d = {}
        for i, value in enumerate(('0123456789' + string.ascii_letters + "-_")):
            d.update({i: value})

    if number == 0:
        b += d[0]

    while number != 0:
        b += d[number % 64]
        number //= 64

    return b[::-1]


d_ = {}


def b64decode(number: str):
    """
    Decode a base64 encoded number to decimal
    :param number: Base64 number as a string
    :return: decoded number
    """
    n = 0
    global d_
    number = list(number)

    if len(d_) < 64:
        d_ = {}
        for i, value in enumerate(('0123456789' + string.ascii_letters + "-_")):
            d_.update({value: i})

    c = 0

    while number:
        try:
            n += d_[number.pop()] * 64**c
        except KeyError:
            return None

        c += 1

    return n


def b64encode_pad(number: int, pad_to: int):
    """
    Encode a number to base64 and pad it to match a specific length
    :param number: Number to encode
    :param pad_to: Minimum size of the number (in characters)
    :return: Encoded and padded number
    """
    number = b64encode(number)
    return ''.join(['0' for _ in range(pad_to - len(number))]) + number
