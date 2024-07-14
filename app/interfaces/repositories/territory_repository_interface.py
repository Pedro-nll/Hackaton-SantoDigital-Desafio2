from abc import ABC, abstractmethod
from entities.territories import Territory

class territories_database_interface(ABC):
    @abstractmethod
    def add_territory(self, territory: Territory):
        pass
    
    @abstractmethod
    def get_territory(self, territory_key: int):
        pass