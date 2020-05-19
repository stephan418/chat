import io
import _io
import hashlib


# Calculates the hash of a file (sha256)
def hash_file(file: io.BufferedReader or _io.BufferedReader, buffer_size: int = 65536) -> str:
    content = file.read(buffer_size)
    file_hash = hashlib.sha256()

    while content:
        file_hash.update(content)
        content = file.read(buffer_size)

    return file_hash.hexdigest()
