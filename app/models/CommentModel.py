from system.core.model import Model

class CommentModel(Model):
    def __init__(self):
        super(CommentModel, self).__init__()

    def get_comments(self, ):
        query = 'SELECT comments.id, message_id, text, comments.created_at, users.id as author_id, users.name as author FROM comments JOIN users ON comments.user_id = users.id';
        return self.db.query_db(query)

    def new_comment(self, comment, message_id, user_id):
        query = 'INSERT INTO comments (text, message_id, user_id, created_at, updated_at) VALUES (:text, :message_id, :user_id, NOW(), NOW())'
        data = {'text': comment, 'message_id': message_id, 'user_id': user_id}
        return self.db.query_db(query, data)

    def validate_comment_author(self, comment_id, user_id):
        query = 'SELECT * FROM comments WHERE id = :id AND user_id = :user_id'
        data = {'id': comment_id, 'user_id': user_id}
        return self.db.query_db(query, data)

    def delete_message_comments(self, message_id):
        query = 'DELETE FROM comments WHERE message_id = :id'
        data = {'id': message_id}
        return self.db.query_db(query, data)

    def delete_comment(self, comment_id):
        query = 'DELETE FROM comments WHERE id = :id'
        data = {'id': comment_id}
        return self.db.query_db(query, data)
