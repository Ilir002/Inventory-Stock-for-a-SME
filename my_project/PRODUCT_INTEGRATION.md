"""Example integration with Product module - Documentation."""

# PRODUCT MODULE INTEGRATION GUIDE

## Relationship Definition

The Category and Product modules have the following relationship:

```
Category (1) ---< Product (Many)
  - One category can have multiple products
  - Each product belongs to exactly one category
  - Category has derived property: product_count
```

## Product Model Integration

When implementing the Product model, add:

```python
# In models/product.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    barcode = Column(String(50), unique=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    current_stock = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=0)
    optimal_stock = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    purchase_cost = Column(Float, nullable=False)
    
    # Relationship back to Category
    category = relationship("Category", back_populates="products")
```

## Service Layer Integration

```python
# In services/product_service.py
from services.category_service import CategoryService

class ProductService:
    def __init__(self, dao: IProductDAO, category_service: CategoryService):
        self.dao = dao
        self.category_service = category_service
    
    def create_product(self, name: str, barcode: str, category_id: int, ...) -> ProductSchema:
        # Validate that category exists
        category = self.category_service.get_category(category_id)
        if not category:
            raise ValueError(f"Category {category_id} not found")
        
        # Create product
        product = self.dao.create(...)
        return ProductSchema.model_validate(product)
    
    def get_product_by_category(self, category_id: int) -> List[ProductSchema]:
        products = self.dao.get_by_category(category_id)
        return [ProductSchema.model_validate(p) for p in products]
```

## UI Integration

### Using CategorySelector in Product Form

```python
# In ui/pages.py for Product module
from ui.components import CategorySelector

@ui.page("/product/create")
async def create_product_page():
    with ui.card():
        # Get all categories for selector
        categories = service.get_all_categories()
        
        # Create selector component
        category_selector = CategorySelector(
            categories=categories,
            label="Product Category"
        )
        selector = category_selector.render()
        
        # Other form fields
        name_input = ui.input(label="Product Name")
        price_input = ui.number(label="Price")
        
        async def save_product():
            category_id = category_selector.get_value()
            if not category_id:
                ui.notify("Please select a category", type="negative")
                return
            
            product_service.create_product(
                name=name_input.value,
                category_id=category_id,
                price=price_input.value,
                ...
            )
```

### Product List with Category Info

```python
@ui.page("/products")
async def products_list():
    products = product_service.get_all_products()
    
    for product in products:
        with ui.card():
            ui.label(product.name)
            ui.label(f"Category: {product.category.name}")  # Access via relationship
            ui.label(f"Tax: {product.category.taxes}%")
            ui.label(f"Price: ${product.price}")
```

## Validation Integration

### Product Schema

```python
# In models/validators.py
from pydantic import BaseModel, Field, field_validator

class ProductSchema(BaseModel):
    product_id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=200)
    barcode: str = Field(..., min_length=5, max_length=50)
    category_id: int  # Existing category ID
    current_stock: int = Field(default=0, ge=0)
    price: float = Field(..., gt=0)
    purchase_cost: float = Field(..., gt=0)
    
    @field_validator("category_id")
    @classmethod
    def validate_category_exists(cls, v, info):
        # This would be called during product creation
        # Category validation happens in ProductService
        return v
```

## Dashboard Integration

### Category Statistics

```python
# In a new dashboard/analytics module
class CategoryAnalytics:
    def __init__(self, category_service: CategoryService, product_service: ProductService):
        self.category_service = category_service
        self.product_service = product_service
    
    def get_category_stats(self) -> List[dict]:
        categories = self.category_service.get_all_categories()
        stats = []
        
        for cat in categories:
            products = self.product_service.get_product_by_category(cat.category_id)
            total_value = sum(p.price * p.current_stock for p in products)
            
            stats.append({
                'category': cat.name,
                'product_count': cat.product_count,
                'total_inventory_value': total_value,
                'tax_rate': cat.taxes
            })
        
        return stats
```

## Testing Product Service with Categories

```python
# In tests/test_product_service.py
import pytest
from services.product_service import ProductService
from services.category_service import CategoryService
from tests.test_category_service import MockCategoryDAO

@pytest.fixture
def product_service():
    # Mock category service
    category_dao = MockCategoryDAO()
    category_svc = CategoryService(category_dao)
    
    # Create test category
    category = category_svc.create_category("Electronics", 19.0)
    
    # Mock product DAO
    product_dao = MockProductDAO()
    product_svc = ProductService(product_dao, category_svc)
    
    return product_svc, category

def test_create_product_with_category(product_service):
    svc, category = product_service
    
    product = svc.create_product(
        name="Laptop",
        barcode="LAPTOP123",
        category_id=category.category_id,
        current_stock=10,
        price=999.99,
        purchase_cost=500.00
    )
    
    assert product.category_id == category.category_id
    assert product.name == "Laptop"
```

## Export/Import Integration

When exporting products, include category information:

```python
def export_products_with_categories(filename: str):
    products = product_service.get_all_products()
    
    rows = []
    for product in products:
        rows.append({
            'product_id': product.product_id,
            'name': product.name,
            'category': product.category.name,
            'tax_rate': product.category.taxes,
            'price': product.price,
            'stock': product.current_stock
        })
    
    # Export to CSV/Excel
```

## API Endpoints Integration (Future)

```python
# In api/routes/products.py (Future REST API)
from fastapi import APIRouter, Depends
from services.category_service import CategoryService

router = APIRouter()

@router.get("/products/by-category/{category_id}")
async def get_products_by_category(
    category_id: int,
    product_service: ProductService = Depends(get_product_service),
    category_service: CategoryService = Depends(get_category_service)
):
    # Verify category exists
    category = category_service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    products = product_service.get_product_by_category(category_id)
    return {
        'category': category,
        'products': products,
        'product_count': len(products)
    }
```

## Summary

The Category module is designed to be integrated seamlessly into the Product module by:

1. **Dependency Injection**: Product service receives Category service
2. **Reusable Components**: CategorySelector component available in Product UI
3. **Validation**: Category existence checked before product creation
4. **Derived Data**: Product count automatically calculated from relationships
5. **Testing**: Mock DAO allows easy testing of both modules independently
