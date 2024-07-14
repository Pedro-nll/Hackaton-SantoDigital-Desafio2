class Sale:
    def __init__(self, orderNumber: str, productKey: int, customerKey: int, territoryKey: int, orderQuantity: int, orderLineItem: int, orderDate: str, stockDate: str): 
        self.orderNumber = orderNumber
        self.productKey = productKey
        self.customerKey = customerKey
        self.territoryKey = territoryKey
        self.orderQuantity = orderQuantity
        self.orderLineItem = orderLineItem
        self.orderDate = orderDate
        self.stockDate = stockDate
