from database.objects.conversation import Conversation
from database.db import MDB


def get_user_conversations(user_id: int, range_from: int, range_to: int, desc: bool = True, _db: MDB = None):
    # TODO: Refactor SQL statement to not yield unused values
    conversations_db = _db.get_cursor() \
        .execute('SELECT id, receiver, sender, date_sent FROM messages WHERE sender = ? or receiver = ? '
                 'ORDER BY date_sent ' + ('desc ' if desc else '') + f'LIMIT {range_to - range_from} ' +
                 f'OFFSET {range_from}', (user_id, user_id))

    already_used = list()
    tmp = list()
    for conversation in conversations_db:
        if not ((conversation[1] != user_id and conversation[1] in already_used)
                or (conversation[2] != user_id and conversation[2] in already_used)):
            if (conversation[1] == conversation[2] and user_id not in already_used) \
                    or conversation[1] != conversation[2]:
                tmp.append(conversation)
                already_used.append(conversation[1] if conversation[1] != user_id else conversation[2])

    conversations = list()
    for conversation in tmp:
        conversations.append(Conversation([conversation[1], conversation[2]], conversation[3]))

    return conversations
