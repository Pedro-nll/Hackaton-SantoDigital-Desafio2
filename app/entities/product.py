class Product:
    def __init__(self, productPrice: float, productKey: int, productSubcategoryKey: int, productSKU: str, productName: str, modelName: str, productDescription: str, productColor: str, productSize: str, productStyle: str, productCost: float):
        self.productPrice = productPrice
        self.productKey = productKey
        self.productSubcategoryKey = productSubcategoryKey
        self.productSKU = productSKU
        self.productName = productName
        self.modelName = modelName
        self.productDescription = productDescription
        self.productColor = productColor
        self.productSize = productSize
        self.productStyle = productStyle
        self.productCost = productCost
