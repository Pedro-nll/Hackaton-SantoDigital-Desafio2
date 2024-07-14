from typing import Union
from schemas.productSubcategorySchema import ProductSubcategorySchema
from pydantic import BaseModel

class ProductSchema(BaseModel):
    product_price: float
    product_key: Union[int, None]
    product_subcategory_key: Union[int, ProductSubcategorySchema]
    product_sku: str
    product_name: str
    product_model_name: str
    product_description: str
    product_color: str
    product_size: str
    product_style: str
    product_cost: float

    class Config:
        from_attributes = True