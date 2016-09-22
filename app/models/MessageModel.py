from system.core.model import Model

class MessageModel(Model):
    def __init__(self):
        super(MessageModel, self).__init__()

    def get_messages(self):
        query = 'SELECT messages.id, text, messages.created_at, users.id as author_id, users.name as author FROM messages JOIN users ON messages.user_id = users.id ORDER BY created_at DESC';
        return self.db.query_db(query)

    def new_message(self, message, user_id):
        query = 'INSERT INTO messages (text, user_id, created_at, updated_at) VALUES (:text, :user_id, NOW(), NOW())'
        data = {'text': message, 'user_id': user_id}
        return self.db.query_db(query, data)

    def validate_message_author(self, message_id, user_id):
        query = 'SELECT * FROM messages WHERE id = :id AND user_id = :user_id'
        data = {'id': message_id, 'user_id': user_id}
        return self.db.query_db(query, data)

    def delete_message(self, message_id):
        query = 'DELETE FROM messages WHERE id = :id'
        data = {'id': message_id}
        return self.db.query_db(query, data)
