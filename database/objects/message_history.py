""" Implementation of the Message history object model """

from database.objects.default import DBObject
from database.objects.message import Message
from security.identification.id import create_unique_id
import time


class MessageHistoryEntry(DBObject):
    """ Handles history entries """
    def __init__(self, entry_id: int, for_message: int, from_text: str or None, from_additional: str or None,
                 creation: int = None):
        if from_text is None and from_additional is None:
            raise ValueError("Both from_text and from_additional are None")

        self.id = entry_id
        self.for_message = for_message
        self.from_text = from_text
        self.from_additional = from_additional
        self.creation = creation or time.time() * 1000

    @staticmethod
    def new(from_message: Message):
        """
        Creates a new instance of MessageHistoryEntry corresponding to the message passed
        :param from_message: The message derived from
        :return: MessageHistoryEntry object
        """
        entry_id = create_unique_id()
        for_message = from_message.id
        from_text = from_message.text_content
        from_additional = from_message.additional_content

        entry = MessageHistoryEntry(entry_id, for_message, from_text, from_additional)

        return entry
