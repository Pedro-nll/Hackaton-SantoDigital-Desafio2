from abc import ABC, abstractmethod
from entities.user import User

class UserUseCaseInterface(ABC):
    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def get_user(self, username: str) -> User:
        pass