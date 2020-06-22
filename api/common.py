from security.encode import number_encode


def encode_if_id(key: str, value, encode: list = None):
    """ Encode and pad the value if it is under the key 'id' """
    if encode is None:
        encode = ['id']

    print(value, key)

    return value if key not in encode else number_encode.b64encode_pad(value, 11)
