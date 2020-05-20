import io
import _io
import hashlib


# Calculates the hash of a file (sha256)
def hash_file(file: io.BufferedReader or _io.BufferedReader, buffer_size: int = 65536) -> str:
    """
    Hash file with the sha256 algorithm
    :param file: Binary read file handler
    :param buffer_size: Size in characters to be read at once
    :return: Hex value of the hash
    """
    content = file.read(buffer_size)
    file_hash = hashlib.sha256()

    # While not returning b""
    while content:
        file_hash.update(content)
        content = file.read(buffer_size)

    return file_hash.hexdigest()
