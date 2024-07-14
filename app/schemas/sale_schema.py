from pydantic import BaseModel

class Sale_schema(BaseModel):
    orderNumber: int
    productKey: int
    customerKey: int
    territoryKey: int
    orderQuantity: int
    orderLineItem: int
    orderDate: str
    stockDate: str
