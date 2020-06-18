""" Message object model """

from database.objects.default import DBObject
from security.identification.id import create_unique_id
import time


class Message(DBObject):
    """
    Object Model of the messages table
    """
    def __init__(self, message_id: int, sender: int, receiver: int,
                 creation: int, date_sent: int, text_content: str = None,
                 blob_content: int = None, date_delivered: int = None, date_read: int = None,
                 last_write: int = None):

        if blob_content is None and text_content is None:
            raise ValueError("Both additional_content and text_content are None")

        self.id = message_id
        self.sender = sender
        self.receiver = receiver
        self.text_content = text_content
        self.additional_content = blob_content
        self.creation = creation
        self.date_sent = date_sent
        self.date_delivered = date_delivered
        self.date_read = date_read
        self.last_write = last_write or creation

    @staticmethod
    def empty():
        """ :return Empty Message """
        return Message(None, None, None, None, None, "")


class Content:
    """
    Handles content. Either text_content or blob_content must be set
    """
    def __init__(self, text_content: str = None, blob_content: int = None):
        if blob_content is None and text_content is None:
            raise ValueError("Both additional_content and text_content are None")

        if len(text_content) > 1000:
            raise ValueError("The length of text_content mustn't be larger than 1000")

        self._text = text_content
        self.blob = blob_content

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        value = str(value)

        if len(value) > 1000:
            raise ValueError("The length of text_content mustn't be larger than 1000")

        self._text = value

    def has_blob_content(self):
        return self.blob is not None

    def has_text_content(self):
        return self.text is not None


def create_message(sender: int, receiver: int, content: Content, date_sent: int):
    """
    Creates a message
    :param sender: ID of the sender of the message
    :param receiver: ID of the message recipient
    :param content: Instance of the content class
    :param date_sent: time.time() * 100 of the time the message was sent
    :return: New instance of Message with the specified values
    """
    message_id = create_unique_id(_db)
    creation = int(time.time() * 1000)

    message = Message(message_id, sender, receiver, creation, date_sent, content.text,
                      content.blob)

    return message
