from flask.json import JSONEncoder


class User:
    def __init__(self, username: str, password: str, user_id: int):
        self.id = user_id
        self.username = username
        self.password = password


class UserEncoder(JSONEncoder):
    def default(self, user: User):
        return user.__dict__
