from typing import Union, Optional
from schemas.productSubcategorySchema import ProductSubcategorySchema
from pydantic import BaseModel

class ProductSchema(BaseModel):
    productPrice: float
    productKey: Optional[int] 
    productSubcategory: Union[int, ProductSubcategorySchema]
    productSKU: str
    productName: str
    modelName: str
    productDescription: str
    productColor: str
    productSize: str
    productStyle: str
    productCost: float

    class Config:
        from_attributes = True