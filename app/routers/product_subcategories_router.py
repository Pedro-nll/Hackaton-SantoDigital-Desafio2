from fastapi import APIRouter, HTTPException
from entities.productSubcategories import ProductSubcategory
from interfaces.usecases.products_subcategories_usecases import ProductSubcategoriesUseCaseInterface
from schemas.productSubcategorySchema import ProductSubcategorySchema

class ProductSubcategoriesRest:
    def __init__(self, product_subcategories_usecase: ProductSubcategoriesUseCaseInterface):
        self.product_subcategories_usecase = product_subcategories_usecase

    def add_routes(self, router: APIRouter):
        router.post("/subcategories/", response_model=dict, tags=["Product Sub-categories"])(self.create_subcategory)
        router.get("/subcategories/{subcategory_id}", response_model=ProductSubcategorySchema, tags=["Product Sub-categories"])(self.get_subcategory)

    async def create_subcategory(self, subcategory: ProductSubcategorySchema):
        subcategory_entity = ProductSubcategory(**subcategory.model_dump())
        self.product_subcategories_usecase.add_product_subcategory(subcategory_entity)
        return {"message": "Subcategory added successfully"}

    async def get_subcategory(self, subcategory_id: int):
        subcategory = self.product_subcategories_usecase.get_product_subcategory(subcategory_id)
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")
        return ProductSubcategorySchema.model_validate(subcategory)

