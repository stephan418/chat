from database.objects.default import DBObject
from security.identification.id import create_unique_id
import time


class Message(DBObject):
    def __init__(self, message_id: int, sender: int, receiver: int,
                 creation: int, date_sent: int, text_content: str = None,
                 additional_content: int = None, date_delivered: int = None, date_read: int = None,
                 last_write: int = None):

        if additional_content is None and text_content is None:
            raise ValueError("Both additional_content and text_content are None")

        self.id = message_id
        self.sender = sender
        self.receiver = receiver
        self.text_content = text_content
        self.additional_content = additional_content
        self.creation = creation
        self.date_sent = date_sent
        self.date_delivered = date_delivered
        self.date_read = date_read
        self.last_write = last_write or creation


class Content:
    def __init__(self, text_content: str = None, additional_content: int = None):
        if additional_content is None and text_content is None:
            raise ValueError("Both additional_content and text_content are None")

        self.text = text_content
        self.additional = additional_content

    def has_additional_content(self):
        return self.additional is not None

    def has_text_content(self):
        return self.text is not None


def create_message(sender: int, receiver: int, content: Content, date_sent: int):
    message_id = create_unique_id()
    creation = int(time.time() * 1000)

    message = Message(message_id, sender, receiver, creation, date_sent, content.text,
                      content.additional)

    return message
