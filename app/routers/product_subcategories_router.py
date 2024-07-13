from fastapi import APIRouter, HTTPException
from entities.productSubcategories import ProductSubcategory
from interfaces.usecases.products_subcategories_usecases import ProductSubcategoriesUseCaseInterface
from schemas.productSubcategorySchema import ProductSubcategorySchema
from schemas.productCategorySchema import ProductCategorySchema

class ProductSubcategoriesRest:
    def __init__(self, product_subcategories_usecase: ProductSubcategoriesUseCaseInterface):
        self.product_subcategories_usecase = product_subcategories_usecase

    def add_routes(self, router: APIRouter):
        router.post("/subcategories/", response_model=dict, tags=["Product Sub-categories"])(self.create_subcategory)
        router.get("/subcategories/{subcategory_id}", response_model=ProductSubcategorySchema, tags=["Product Sub-categories"])(self.get_subcategory)

    async def create_subcategory(self, subcategory: ProductSubcategorySchema):
        if isinstance(subcategory.product_category_key, ProductCategorySchema):
            product_category_key = subcategory.product_category_key.product_category_key
        else:
            product_category_key = subcategory.product_category_key

        subcategory_entity = ProductSubcategory(
            product_subcategory_key=subcategory.product_subcategory_key,
            product_category_key=product_category_key,
            subcategory_name=subcategory.subcategory_name
        )

        self.product_subcategories_usecase.add_product_subcategory(subcategory_entity)
        return {"message": "Subcategory added successfully"}


    async def get_subcategory(self, subcategory_id: int):
        subcategory = self.product_subcategories_usecase.get_product_subcategory(subcategory_id)
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")
        
        subcategory_schema = ProductSubcategorySchema(
            product_subcategory_key = subcategory.product_category_key,
            subcategory_name = subcategory.subcategory_name,
            product_category_key = subcategory.product_subcategory_key
        )
        return ProductSubcategorySchema.model_validate(subcategory_schema)

