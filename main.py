import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_init import get_session
from database.models import ProductModels
from schemas.schemas import ProductsSchema

app = FastAPI(title="bereg API",
              summary="API for working with products with PostgreSQL (parse data) ",
              version="latest")


@app.get("/products/", summary='Получить все продукты из базы данных', tags=['Products'])
async def get_all_products(db: AsyncSession = Depends(get_session)) -> list[ProductsSchema]:
    """
    Get all products from the database
    Получить все продукты из базы данных
    """
    query = select(ProductModels)
    result = await db.execute(query)
    products_data = result.scalars().all()
    products = [ProductsSchema.model_validate(item, from_attributes=True) for item in products_data]
    return products


@app.get("/products/{id}", summary='Получить продукт по ID', tags=['Products'])
async def get_product_by_id(id: int, db: AsyncSession = Depends(get_session)) -> ProductsSchema:
    """
    Get product by ID from the database
    Получить продукт по ID из базы данных
    """
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    query = select(ProductModels).where(ProductModels.id == id)
    result = await db.execute(query)
    product_data = result.scalars().first()
    product = ProductsSchema.model_validate(product_data, from_attributes=True)
    return product


@app.get('/categories/', summary='Получить все категории товаров', tags=['Categories'])
async def get_products_category(db: AsyncSession = Depends(get_session)) -> dict[str, list[str]]:
    """
    Get all categories of products
    Получить все категории товаров
    """
    query = select(distinct(ProductModels.product_name))
    categories = await db.execute(query)
    categories = categories.scalars().all()
    return {'categories': categories}


@app.get('/categories/{category_name}', summary='Получить все продукты по категории', tags=['Categories'])
async def get_products_by_category(category_name: str, db: AsyncSession = Depends(get_session)) -> list[ProductsSchema]:
    """
    Get all products by category
    Получить все продукты по категории
    """
    query = select(ProductModels).where(ProductModels.product_name == category_name)
    result = await db.execute(query)
    products_data = result.scalars().all()
    products = [ProductsSchema.model_validate(item, from_attributes=True) for item in products_data]
    if products == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return products


@app.get('/items/', summary='Получить все названия товаров', tags=['Items'])
async def get_products_item_name(db: AsyncSession = Depends(get_session)) -> dict[str, list[str]]:
    """
    Get all product names
    Получить все названия товаров
    """
    query = select(distinct(ProductModels.item_name))
    items = await db.execute(query)
    items = items.scalars().all()
    return {'items': items}


@app.get('/items/{item_name}', summary='Получить все продукты по названию', tags=['Items'])
async def get_product_by_item_name(item_name: str, db: AsyncSession = Depends(get_session)) -> list[ProductsSchema]:
    """
    Get all products by name
    Получить все продукты по названию
    """
    query = select(ProductModels).where(ProductModels.item_name == item_name)
    result = await db.execute(query)
    products_data = result.scalars().all()
    products = [ProductsSchema.model_validate(item, from_attributes=True) for item in products_data]
    if products == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return products


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
