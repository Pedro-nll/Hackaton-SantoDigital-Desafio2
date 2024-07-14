from entities.user import User
from interfaces.repositories.user_repository_interface import UserDatabaseInterface
from interfaces.usecases.user_usecase_interface import UserUseCaseInterface

class UserUseCase(UserUseCaseInterface):
    def __init__(self, repository: UserDatabaseInterface):
        self.repository = repository

    def add_user(self, user: User):
        self.repository.add_user(user)

    def get_user(self, username: str) -> User:
        return self.repository.get_user(username)