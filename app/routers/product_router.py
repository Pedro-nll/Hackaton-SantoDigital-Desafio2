from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from entities.product import Product
from interfaces.usecases.productsUsecasesInterface import ProductsUsecasesInterface
from schemas.productSchema import ProductSchema
from schemas.productSubcategorySchema import ProductSubcategorySchema
from schemas.productCategorySchema import ProductCategorySchema
from schemas.OutputProductSubcategorySchema import OutputProductSubcategorySchema
from schemas.OutputProductSchema import OutputProductSchema
from config.JWTUtility import get_current_admin_user, get_current_user

class ProductsRest:
    def __init__(self, product_usecases: ProductsUsecasesInterface):
        self.product_usecases = product_usecases

    def add_routes(self, router: APIRouter):
        router.post(
            "/products/",
            response_model=dict,
            tags=["Product"],
            dependencies=[Depends(get_current_admin_user)]
        )(self.create_product)
        router.delete(
            "/products/{product_id}",
            response_model=dict,
            tags=["Product"],
            dependencies=[Depends(get_current_admin_user)]
        )(self.delete_product)
        router.put(
            "/products/{product_key}",
            response_model=dict,
            tags=["Product"],
            dependencies=[Depends(get_current_admin_user)]
        )(self.update_product)
        router.get("/products/{product_key}", response_model=ProductSchema, tags=["Product"])(self.get_product)
        router.get("/products/", response_model=List[ProductSchema], tags=["Product"])(self.get_all_products)

    async def create_product(self, product: ProductSchema, current_user = Depends(get_current_admin_user)):
        product_subcategory = product.product_subcategory_key
        if isinstance(product_subcategory, ProductSubcategorySchema):
            product_subcategory = product_subcategory.product_subcategory_key

        product_entity = Product(
            product_key = product.product_key,
            product_price = product.product_price,
            product_subcategory_key = product_subcategory,
            product_sku = product.product_sku,
            product_name = product.product_name,
            model_name = product.product_model_name,
            product_description = product.product_description,
            product_color = product.product_color,
            product_size = product.product_size,
            product_style = product.product_style,
            product_cost = product.product_cost
        )

        self.product_usecases.add_product(product_entity, current_user)
        return {"message": "Product added successfully"}


    async def delete_product(self, product_id: int, current_user = Depends(get_current_admin_user)):
        self.product_usecases.delete_product(product_id, current_user)
        return {"message": "Product deleted successfully"}

    async def update_product(self, product_key: int, product: ProductSchema, current_user = Depends(get_current_admin_user)):
        product_entity = Product(
                product_key=product_key, 
                product_price = product.product_price,
                product_subcategory_key = product.product_subcategory_key,
                product_sku = product.product_sku,
                product_name = product.product_name,
                model_name = product.product_model_name,
                product_description = product.product_description,
                product_color = product.product_color,
                product_size = product.product_size,
                product_style = product.product_style,
                product_cost = product.product_cost
            )
        self.product_usecases.update_product(product_entity, current_user)
        return {"message": "Product updated successfully"}

    async def get_product(self, product_key: int):
        product = self.product_usecases.get_product(product_key)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        category_schema = ProductCategorySchema(
            category_name=product.product_subcategory_key.product_category_key.category_name,
            product_category_key=product.product_subcategory_key.product_category_key.product_category_key
        )
        
        subcategory_schema = OutputProductSubcategorySchema(
            product_subcategory_key=product.product_subcategory_key.product_subcategory_key,
            subcategory_name=product.product_subcategory_key.subcategory_name,
            product_category_key=category_schema
        )
        
        p = OutputProductSchema(
            product_key=product.product_key,
            product_price=product.product_price,  
            product_subcategory_key=subcategory_schema,
            product_sku=product.product_sku,
            product_name=product.product_name,
            product_model_name=product.model_name,
            product_description=product.product_description,
            product_color=product.product_color,
            product_size=product.product_size,
            product_style=product.product_style,
            product_cost=product.product_cost
        )
        return OutputProductSchema.model_validate(p)

    async def get_all_products(
        self,
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0),
        sort_by: Optional[str] = Query(None, regex="^(product_key|product_price|product_name)$"),
        sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
        filter_by: Optional[str] = Query(None),
        filter_value: Optional[str] = Query(None)
    ):
        products = self.product_usecases.get_all_products()

        # FILTRAGEM
        if filter_by and filter_value:
            products = [product for product in products if getattr(product, filter_by) == filter_value]

        # ORDENAÇÃO
        if sort_by:
            reverse = sort_order == "desc"
            products.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)

        # PAGINAÇÃO
        products = products[offset:offset + limit]

        products_schema_list = []
        for product in products:
            category_schema = ProductCategorySchema(
                category_name=product.product_subcategory_key.product_category_key.category_name,
                product_category_key=product.product_subcategory_key.product_category_key.product_category_key
            )

            subcategory_schema = OutputProductSubcategorySchema(
                product_subcategory_key=product.product_subcategory_key.product_subcategory_key,
                subcategory_name=product.product_subcategory_key.subcategory_name,
                product_category_key=category_schema
            )

            p = OutputProductSchema(
                product_key=product.product_key,
                product_price=product.product_price,
                product_subcategory_key=subcategory_schema,
                product_sku=product.product_sku,
                product_name=product.product_name,
                product_model_name=product.model_name,
                product_description=product.product_description,
                product_color=product.product_color,
                product_size=product.product_size,
                product_style=product.product_style,
                product_cost=product.product_cost
            )
            products_schema_list.append(p)

        return [OutputProductSchema.model_validate(product) for product in products_schema_list]
