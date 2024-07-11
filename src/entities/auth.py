from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class User:
    def __init__(self, user_id: int, username: str, password_hash: str, role: Role):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
