from pydantic import BaseModel
from schemas.OutputProductSubcategorySchema import OutputProductSubcategorySchema

class OutputProductSchema(BaseModel):
    product_key: int
    product_price: float
    product_subcategory_key: OutputProductSubcategorySchema
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