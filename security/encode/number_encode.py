import string


d = {}  # Dictionary to cache the value generated in the next function


# Encode number to base64
def b64encode(number: int):
    b = ""
    global d

    if len(d) < 64:
        d = {}
        for i, value in enumerate(('0123456789' + string.ascii_letters + "@+-")):
            d.update({i: value})

    if number == 0:
        b += d[0]

    while number != 0:
        b += d[number % 64]
        number //= 64

    return b[::-1]