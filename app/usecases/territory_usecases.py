from interfaces.usecases.territories_usecases_interface import Territory_usecases_interface
from interfaces.repositories.territory_repository_interface import territories_database_interface
from entities.territories import Territory

class Territory_usecases(Territory_usecases_interface):
    def __init__(self, repository: territories_database_interface):
        self.repository = repository
   
    def add_territory(self, territory: Territory):
        self.repository.add_territory(territory)

    def get_territory(self, territory_key: int) -> Territory:
        return self.repository.get_territory(territory_key)