""" Actions for objects in the blob storage """

from database.objects.blob import Blob
from database.main_db import db
from security.identification.id import create_unique_id
import os


def add_to_storage(current_path: str, content_type: int, author: int, _db=db):
    if not _db.entry_exists_eq("users", "id", author):
        raise ValueError("The author specified does not exist")

    allowed_extensions = [".txt", ".png", ".jpg", ".jpeg", ".gif", ".mp3", ".mp4"]

    _, extension = os.path.splitext(current_path)

    if extension not in allowed_extensions:
        raise ValueError(f"The file extension '{extension}' is not allowed")

    blob_id = create_unique_id()

    blob = Blob(blob_id, content_type, author)

    fs_path = blob.register_file(current_path, _db=_db)

    return fs_path
