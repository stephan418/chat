""" Conversation object Model. """
# As conversation are an abstraction not present in the DB itself,
# they don't have an identifier and cannot be accessed on a individually.
# Therefore, they can only be accessed by impersonating on of the owners.

# TODO: Groups (Maybe rethink DB abstraction to allow for multiple receivers - Broadcasts)

from database.objects.default import DBObject


class Conversation(DBObject):
    def __init__(self, participants: list, last_activity: int):
        self.participants = participants
        # TODO: latest messages
        self.last_activity = last_activity

    @staticmethod
    def empty(self):
        return Conversation(None, None)
