from system.core.model import Model
import re


class UserModel(Model):
    def __init__(self):
        super(UserModel, self).__init__()

    def create(self, name, email, password):
        query = "INSERT INTO Users (name, email, password, created_at, updated_at) VALUES (:name, :email, :password, NOW(), NOW())"
        data = {'name': name,'email': email, 'password': password}
        return self.db.query_db(query, data)

    def get_by_email(self, email):
        query = 'SELECT * FROM users WHERE email = :email'
        data = {'email': email}
        return self.db.query_db(query, data)

    def login(self, post):
        email = post['email'].lower()
        password = post['password']
        if email and password:
            user = self.get_by_email(email)
            if user:
                if self.bcrypt.check_password_hash(user[0]['password'], password):
                    return user
        return []

    def register(self, post):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        name = post['name'].lower()
        email = post['email'].lower()
        password = post['password']
        passwordConfirm = post['passwordConfirm']

        err = {}
        if not name:
            err['name'] = "Name cannot be blank"
        if not email:
            err['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(email):
            err['email'] = "Invalid email address"
        if not password:
            err['password'] = "Password cannot be blank"
        if not passwordConfirm:
            err['passwordConfirm'] = "Password Confirmation cannot be blank"
        if password and passwordConfirm and password != passwordConfirm:
            err['password'] = "Passwords do not match"

        if not err:
            if not self.get_by_email(email):
                encrypted_password = self.bcrypt.generate_password_hash(password)
                user_id = self.create(name, email,encrypted_password)
                return {'user_id': user_id}
            return {'errors': {'email': "Invalid email address"}}
        return {'errors': err}
