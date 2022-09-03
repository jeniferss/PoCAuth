from model.user import User

USERS: [User] = [User(username='user.demo', password='password', user_id=1),
                 User(username='admin.user', password='password', user_id=2)]


def get_user(username: str, password: str):
    for user in USERS:
        if user.username == username:
            if user.password == password:
                return user
    return None
