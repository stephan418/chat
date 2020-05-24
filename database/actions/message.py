from database.objects import message
from database.main_db import db
from security.identification.id import create_unique_id
import time


def create_message(sender: int, receiver: int, content: message.Content, date_sent: int, _db=db):
    """
    Create new message and insert it into the database
    :param sender: ID of the sender (must exist)
    :param receiver: ID of the receiver (must exist)
    :param content: Content object
    :param date_sent: Date and time when the message was sent (Warning: Mustn't be more than 1 hour earlier than time()
    :param _db: The database cursor (Default is most-likely ok, just for testing
    :return: Newly created message
    """
    message_id = create_unique_id()
    creation = int(time.time() * 1000)

    if not _db.entry_exists_eq("users", "id", sender):
        raise ValueError(f"The sender (ID '{sender}') does not exist")

    if not _db.entry_exists_eq("users", "id", receiver):
        raise ValueError(f"The receiver (ID '{receiver}') does not exist")

    msg = message.Message(message_id, sender, receiver, creation, date_sent, content.text, content.blob)

    _db.insert_all_values(msg, "messages")

    return msg


def delete_message(msg_id: int):
    db
