from pydantic import BaseModel

class Sale_schema(BaseModel):
    orderNumber: str
    productKey: int
    customerKey: int
    territoryKey: int
    orderQuantity: int
    orderLineItem: int
    orderDate: str
    stockDate: str
