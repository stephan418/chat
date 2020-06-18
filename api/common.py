from security.encode import number_encode


def encode_if_id(key: str, value):
    """ Encode and pad the value if it is under the key 'id' """
    return value if key != 'id' else number_encode.b64encode_pad(value, 11)
