from pydantic import BaseModel

class ProductCategorySchema(BaseModel):
    product_category_key: int
    category_name: str