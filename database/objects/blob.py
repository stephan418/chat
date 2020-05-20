""" Implementation of the Blob object model """

from database.objects.default import DBObject
from security.identification.id import create_unique_id
from security.encode.number_encode import b64encode
from security.hash.file import hash_file
import os
import shutil
import time
from database.main_db import db
import filecmp


def file_equals_blob(file, fs_path):
    return filecmp.cmp(file, os.environ['BLOB_STORAGE'] + fs_path)


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
    """
    This class represents data stored in the blob storage of the database.
    The blob storage is file system storage kept track of by the database to store binary file or large text.
    """
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
        """
        Register a file in the blob storage and in the class instance.
        The original file will be deleted
        :param path: Current path of the file
        :return: blob storage path of the file
        """
        if self.fs_path is not None:
            raise ValueError("File already registered and saved!")

        if not os.path.exists(path):
            raise FileNotFoundError("The file which is trying to be added doesn't exist")

        with open(path, "rb") as file:
            file_hash = hash_file(file)

        identical = db.get_all_elements_eq("blobs", "hash", file_hash, "id, fs_path")
        values = None

        # TODO: Add check for type, so that a file as img isn't treated the same as txt with the same content
        if identical is not None:
            for item in identical:
                fs_path = item[1]

                if file_equals_blob(path, fs_path):
                    values = db.get_all_elements_eq("blobs", "id", item[0], columns="id, type, fs_path, author, hash")

        if values is not None:
            self.__init__(values[0], values[1], values[3], values[4], values[2])
            return values[2]

        fs_path = self._generate_id()

        self.fs_path = fs_path
        self.hash = file_hash

        self._move_to_blob_storage(path, fs_path)

        return fs_path

    @staticmethod
    def _move_to_blob_storage(src, fs_path):
        """
        This function moves files to the blob storage (specified in environment variable "BLOB_STORAGE".
        :param src: Current path of the file
        :param fs_path: Path in the blob storage (Blob._generate_id)
        """
        shutil.move(src, os.environ['BLOB_STORAGE'] + fs_path, copy_function=shutil.copy)

    @staticmethod
    def _generate_id():
        """
        Generates path for storage in the blob storage (unique)
        :return: Generated path
        """
        path = "."

        # Using GMT
        gmtime = time.gmtime()

        # Make sure the path isn't already used TODO: Shouldn't actually happen (Test on multiple threads or processes)
        while os.path.exists(path):
            path = f'{os.environ["BLOB_STORAGE"]}/{gmtime.tm_year}-{gmtime.tm_mon}/{gmtime.tm_mday}/' \
                   f'{gmtime.tm_hour}/{b64encode(create_unique_id())}.blob'

        return path

    def _add_to_db(self):
        db.insert_all_values(self, "blobs")
