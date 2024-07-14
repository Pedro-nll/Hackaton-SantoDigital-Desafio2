from fastapi import APIRouter
from interfaces.usecases.territories_usecases_interface import Territory_usecases_interface
from schemas.territory_schema import Territory_schema
from entities.territories import Territory

class Territory_rest:
    def __init__(self, territory_usecases: Territory_usecases_interface):
        self.territory_usecases = territory_usecases
        
    def add_routes(self, router: APIRouter):
        router.post("/territories/", response_model=dict, tags=["Territories"])(self.add_territory)
    
    async def add_territory(self, territory: Territory_schema):
        territory_entity = Territory(**territory.model_dump())
        self.territory_usecases.add_territory(territory_entity)
        return {"message": "Territory added successfully"}