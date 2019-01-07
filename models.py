from flask import abort


class UserDAO:
    def __init__(self):
        self.counter = 0
        self.users = []

    def get(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        abort(404, "User {} doesn't exist".format(id))

    def create(self, data):
        user = data
        user['id'] = self.counter = self.counter + 1
        self.users.append(user)
        return user

    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user

    def delete(self, id):
        user = self.get(id)
        self.users.remove(user)

