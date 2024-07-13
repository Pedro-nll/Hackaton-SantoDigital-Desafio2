# SO OS 5 PRIMEIROS PRODUTOS
for index, row in products_df.head(5).iterrows():
    # Pra inicializar os produtos preciso primeiro das categorias deles
    # pra inicializar as cat preciso primeiro das subcat
    subcategory_key = row['ProductSubcategoryKey']
    subcategory_row = subcategories_df[subcategories_df['ProductSubcategoryKey'] == subcategory_key].iloc[0]

    category_key = subcategory_row['ProductCategoryKey']
    category_row = categories_df[categories_df['ProductCategoryKey'] == category_key].iloc[0]

    # inicializo um objeto pras categorias
    category = ProductCategorySchema(
        product_category_key=category_row['ProductCategoryKey'],
        category_name=category_row['CategoryName']
    )
    # mando a categoria pra api
    post_category(category.product_category_key, category.category_name)

    # inicializo subcat de dois jeitos:
    # 1. Com a key da categoria mae
    # 2. com o objeto da cat mae
    # pra testar ambos comportamentos
    subcategory = ProductSubcategorySchema(
        product_subcategory_key=subcategory_row['ProductSubcategoryKey'],
        subcategory_name=subcategory_row['SubcategoryName'],
        product_category_key=category if index == 1 else category_key
    )
    # mando pra api
    post_subcategory(subcategory.product_subcategory_key, subcategory.subcategory_name, subcategory.product_category_key)

    # quero testar os comportamentos de 3 jeitos:
    # com a subcategoria sendo só a key
    # com a subcat sendo o objeto tendo a key da categoria mae
    # com a subcat sendo o objeto com o objeto da cat dentro (em teória não deve alterar nada na API, mas não doí testar)