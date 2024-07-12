from typing import Union
from schemas.productCategorySchema import ProductCategorySchema
from pydantic import BaseModel

class ProductSubcategorySchema(BaseModel):
    product_subcategory_key: int
    subcategory_name: str
    product_category_key: Union[int, ProductCategorySchema]