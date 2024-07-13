class Product:
    def __init__(self, product_price: float, product_key: int, product_subcategory_key: int, product_sku: str, product_name: str, model_name: str, product_description: str, product_color: str, product_size: str, product_style: str, product_cost: float):
        self.product_price = product_price
        self.product_key = product_key
        self.product_subcategory_key = product_subcategory_key
        self.product_sku = product_sku
        self.product_name = product_name
        self.model_name = model_name
        self.product_description = product_description
        self.product_color = product_color
        self.product_size = product_size
        self.product_style = product_style
        self.product_cost = product_cost
