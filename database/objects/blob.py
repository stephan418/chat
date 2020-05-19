from database.objects.default import DBObject


class Blob(DBObject):
    def __init__(self, blob_id: int, blob_type: int, path: str, author: int, blob_hash: int):
        if not 0 <= blob_type <= 5:
            raise ValueError(f"{blob_type} is not a valid type id (0-5)")

        self.id = blob_id
        self.type = blob_type
        self.fs_path = path
        self.author = author
        self.hash = blob_hash
