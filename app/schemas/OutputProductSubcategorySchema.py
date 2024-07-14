from pydantic import BaseModel
from schemas.productCategorySchema import ProductCategorySchema

class OutputProductSubcategorySchema(BaseModel):
    product_subcategory_key: int
    subcategory_name: str
    product_category_key: ProductCategorySchema