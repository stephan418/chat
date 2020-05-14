# conn = sqlite3.connect("storage.db")
#
#
# class Message:
#     def __init__(self, content, recipient_id):
#         self.content = content
#         self.recipient_id = recipient_id
#         self.length = len(self.content)
#
#
# message = Message('Hallo', 100)
# message2 = Message('Hello back', 101)
#
#
# cursor = conn.cursor()
#
# cursor.execute(f"INSERT INTO messages (content, length, recipient) VALUES ('{message.content}', {message.length}, "
#                f"{message.recipient_id})")
# print(cursor.execute("SELECT * FROM messages WHERE id=(SELECT MAX(id) FROM messages)").fetchall())
#
# conn.commit()
#
# conn.close()
