from pydantic import BaseModel, Field


class ProductsSchema(BaseModel):
    id: int = Field(..., description="The product ID.")
    product_name: str = Field(..., min_length=2, man_length=150, description="The product name.")
    category_name: str = Field(..., min_length=2, man_length=150, description="The category name.")
    item_name: str = Field(..., min_length=2, man_length=150, description="The item name.")
    price: float = Field(..., gt=0, description="The product price.")
    density: float = Field(..., gt=0, description="The product density.")
    size: str = Field(..., min_length=2, man_length=15, description="The product size.")
    quantity: str = Field(..., min_length=2, man_length=15, description="The product quantity.")
