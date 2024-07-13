from fastapi import APIRouter, HTTPException
from entities.productCategories import ProductCategory
from interfaces.usecases.products_categories_usecases import ProductCategoriesUseCaseInterface
from schemas.productCategorySchema import ProductCategorySchema

class ProductCategoriesRest:
    def __init__(self, product_categories_usecase: ProductCategoriesUseCaseInterface):
        self.product_categories_usecase = product_categories_usecase

    def add_routes(self, router: APIRouter):
        router.post("/categories/", response_model=dict, tags=["Product Categories"])(self.create_category)
        router.get("/categories/{category_id}", response_model=ProductCategorySchema, tags=["Product Categories"])(self.get_category)

    async def create_category(self, category: ProductCategorySchema):
        category_entity = ProductCategory(**category.model_dump())
        self.product_categories_usecase.add_product_category(category_entity)
        return {"message": "Category added successfully"}

    async def get_category(self, category_id: int):
        category = self.product_categories_usecase.get_product_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        category_schema = ProductCategorySchema(
            category_name= category.category_name,
            product_category_key= category.product_category_key
        )
        return ProductCategorySchema.model_validate(category_schema)
