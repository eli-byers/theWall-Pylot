from system.core.controller import *

class Wall(Controller):
    def __init__(self, action):
        super(Wall, self).__init__(action)
        self.load_model('MessageModel')
        self.load_model('CommentModel')
        self.load_model('UserModel')
        self.db = self._app.db


    # -----------------------  User  -----------------------------
    def login(self):
        post = request.form
        if 'email' in post and 'password' in post:
            if post['email'] and post['password']:
                user = self.models['UserModel'].login(post)
                if user:
                    session['user_id'] = int(user[0]['id'])
                    session['name'] = user[0]['name']
                    return redirect('/wall')
                flash("Email and password do not match", 'lg_email')
            else:
                if not post['email']: flash("Email cannot be blank", 'lg_email')
                if not post['password']: flash("Password cannot be blank", 'lg_password')
        return redirect('/')

    def register(self):
        post = request.form
        if 'name' in post and 'email' in post and 'password' in post and 'passwordConfirm' in post:
            data = self.models['UserModel'].register(post)
            if 'errors' in data:
                for error in data['errors']:
                    flash(data['errors'][error], error)
            else:
                print data
                print data['user_id']
                session['user_id'] = int(data['user_id'])
                session['name'] = post['name'].lower().title()
                return redirect('/wall')
        return redirect('/')

    def logout(self):
        session.pop('user_id', None)
        session.pop('name', None)
        return redirect('/')


    # -----------------------  Render  -----------------------------
    def index(self):
        if 'user_id' in session and 'name' in session:
            return redirect('/wall')
        return self.load_view('index.html')

    def wall(self):
        if 'user_id' in session and 'name' in session:
            messages = self.models['MessageModel'].get_messages()
            comments = self.models['CommentModel'].get_comments()
            return self.load_view('wall.html', messages=messages, comments=comments)
        return redirect ('/')


    # -----------------------  Messages  -----------------------------
    def new_message(self):
        post = request.form
        if 'message' in post:
            self.models['MessageModel'].new_message(post['message'], session['user_id'])
        return redirect('/wall')

    def delete_message(self, message_id):
        if self.models['MessageModel'].validate_message_author(message_id, session['user_id']):
            self.models['CommentModel'].delete_message_comments(message_id)
            self.models['MessageModel'].delete_message(message_id)
        return redirect('/wall')


    # -----------------------  Comments  -----------------------------
    def new_comment(self):
        post = request.form
        if 'text' in post and 'message_id' in post:
            self.models['CommentModel'].new_comment(post['text'], post['message_id'], session['user_id'])
        return redirect('/wall')

    def delete_comment(self, comment_id):
        if self.models['CommentModel'].validate_comment_author(comment_id, session['user_id']):
            self.models['CommentModel'].delete_comment(comment_id)
        return redirect('/wall')
