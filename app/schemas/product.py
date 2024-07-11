from pydantic import BaseModel

class ProductSchema(BaseModel):
    product_id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True
