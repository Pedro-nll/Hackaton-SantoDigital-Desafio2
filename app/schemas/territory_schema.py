from pydantic import BaseModel

class Territory_schema(BaseModel):
    salesTerritoryKey: int
    region: str
    country: str
    continent: str
