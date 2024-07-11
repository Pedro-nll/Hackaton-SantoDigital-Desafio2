class Sale:
    def __init__(self, sale_id: int, product_id: int, customer_id: int, quantity: int, sale_date: str):
        self.sale_id = sale_id
        self.product_id = product_id
        self.customer_id = customer_id
        self.quantity = quantity
        self.sale_date = sale_date
