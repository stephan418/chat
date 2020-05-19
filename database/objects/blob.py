from database.objects.default import DBObject
from security.identification.id import create_unique_id
from security.encode.number_encode import b64encode
import os
import shutil
import time
from database.main_db import db
import hashlib


# Blob class for storing general information.
#
# Types:
#   0: text/plain       Plain text files (.txt)
#   1: image/png        PNG image
#   2: image/jpeg       JPEG image
#   3: image/gif        GIF image
#   4: audio/internal   Audio recorded with the internal audio recorder
#   5: audio/mpeg       Regular Audio (.mp3)
#   6: video/mp4        MP4 Video file (.mp4)

class Blob(DBObject):
    def __init__(self, blob_id: int, blob_type: int, author: int, blob_hash: int = None, path: str = None):
        if not 0 <= blob_type <= 5:
            raise ValueError(f"{blob_type} is not a valid type id (0-5)")

        self.id = blob_id
        self.type = blob_type
        self.fs_path = path
        self.author = author
        self.hash = blob_hash

    # Register a file in the blob storage
    def register_file(self, path):
        # Don't execute if the file path is already set
        if self.fs_path is not None:
            raise ValueError("File already registered and saved!")

        if not os.path.exists(path):
            raise FileNotFoundError("The file which is trying to be added doesn't exist")

        path = self._generate_id()

    # Copies the specified file to the blob storage
    @staticmethod
    def _copy_to_blob_storage(src, fs_path):
        shutil.move(src, os.environ['BLOB_STORAGE'] + fs_path, copy_function=shutil.copy)

    @staticmethod
    def _generate_id():
        path = "."

        while os.path.exists(path):
            # Using GMT
            gmtime = time.gmtime()

            path = f'{os.environ["BLOB_STORAGE"]}/{gmtime.tm_year}-{gmtime.tm_mon}/{gmtime.tm_mday}/' \
                   f'{gmtime.tm_hour}/{b64encode(create_unique_id())}.blob'

        return path
