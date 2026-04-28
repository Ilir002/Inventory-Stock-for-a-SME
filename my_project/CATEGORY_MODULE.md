"""Documentation for Category Module."""

# Category Module - Architecture & Implementation Guide

## Overview

The Category module implements a complete inventory category management system following SOLID and DRY principles with Object-Oriented Programming.

## Architecture Layers

### 1. Models Layer (`models/`)
- **category.py**: Category ORM model (placeholder, will be implemented with SQLAlchemy)
- **validators.py**: Pydantic schemas for validation
  - `CategorySchema`: Full category data representation
  - `CategoryCreateRequest`: Request validation for creation
  - `CategoryUpdateRequest`: Request validation for updates

### 2. DAO Layer (`dao/`)
- **base.py**: Abstract interface `ICategoryDAO` defining all data access contracts
- **category_dao.py**: SQL implementation (placeholder, ready for SQLAlchemy)

The DAO layer follows the **Repository Pattern** and **Dependency Injection** principle, allowing easy swapping of implementations.

### 3. Service Layer (`services/`)
- **category_service.py**: `CategoryService` class with business logic
  - CRUD operations: create, read, update, delete
  - Search and filtering
  - Validation orchestration
  - Product count aggregation

### 4. UI Layer (`ui/`)
- **components.py**: Reusable NiceGUI components
  - `CategorySelector`: Dropdown component for category selection
  - `CategoryForm`: Reusable form component
  - `CategoryCard`: Display component with actions
  
- **pages.py**: Page definitions for NiceGUI application
  - List page: View all categories with search
  - Create page: Add new category
  - Edit page: Modify existing category
  - Delete confirmation dialog

### 5. Tests (`tests/`)
- **test_validators.py**: Validation schema tests
- **test_category_service.py**: Service layer tests with MockCategoryDAO

## Design Principles Applied

### SOLID
- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Classes open for extension, closed for modification
- **L**iskov Substitution: DAO interface ensures consistent behavior
- **I**nterface Segregation: Clean, focused interfaces
- **D**ependency Inversion: Depends on abstractions (ICategoryDAO), not implementations

### DRY (Don't Repeat Yourself)
- Reusable components in UI layer
- Centralized validation using Pydantic
- Abstract DAO interface prevents duplication

## Key Features

### Validation
- Category name uniqueness validation
- Name length constraints (2-100 characters)
- Tax rate range validation (0-100%)
- Automatic whitespace trimming
- Pydantic error messages

### Service Methods
```python
# CRUD
service.create_category(name, taxes)
service.get_category(category_id)
service.get_all_categories()
service.update_category(category_id, name, taxes)
service.delete_category(category_id)

# Search & Filter
service.search_categories(query)
service.get_categories_with_products()
service.get_categories_without_products()
```

### UI Pages
- `/` - Home page
- `/categories` - List all categories with search
- `/category/create` - Add new category
- `/category/edit/{category_id}` - Edit category

## Testing

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=services --cov=models --cov=dao

# Specific test file
pytest tests/test_category_service.py

# Specific test class
pytest tests/test_category_service.py::TestCategoryServiceCreate
```

### Test Coverage
- **test_validators.py**: Pydantic validation rules
- **test_category_service.py**: All service methods and edge cases
- **MockCategoryDAO**: In-memory implementation for testing

## Integration Points

### Database Integration (Pending)
When SQL is implemented:
1. Create `CategoryDAOSQL` implementing `ICategoryDAO` using SQLAlchemy
2. Update main.py to use real DAO instead of MockCategoryDAO
3. No changes needed in service or UI layers

### Product Integration
Categories relate to Products via:
- One-to-Many relationship: One Category has Many Products
- `product_count` property: Automatically calculated from related products
- Category selector component available for Product forms

## Usage Example

```python
from services.category_service import CategoryService
from tests.test_category_service import MockCategoryDAO

# Initialize
dao = MockCategoryDAO()  # Replace with CategoryDAOSQL later
service = CategoryService(dao)

# Create
category = service.create_category("Electronics", 19.0)
print(f"Created: {category.name}")

# Read
all_cats = service.get_all_categories()
for cat in all_cats:
    print(f"{cat.name}: {cat.product_count} products")

# Update
updated = service.update_category(category.category_id, "Tech", 21.0)

# Search
results = service.search_categories("tech")

# Delete
service.delete_category(category.category_id)
```

## File Structure

```
my_project/
├── models/
│   ├── __init__.py
│   ├── category.py (ORM placeholder)
│   ├── product.py (stub)
│   ├── order.py (stub)
│   ├── order_line.py (stub)
│   ├── invoice.py (stub)
│   └── validators.py (Pydantic schemas)
├── dao/
│   ├── __init__.py
│   ├── base.py (ICategoryDAO interface)
│   ├── category_dao.py (SQL implementation placeholder)
│   ├── product_dao.py (stub)
│   └── ...
├── services/
│   ├── __init__.py
│   └── category_service.py (CategoryService)
├── ui/
│   ├── __init__.py
│   ├── components.py (NiceGUI components)
│   └── pages.py (Page definitions)
├── tests/
│   ├── __init__.py
│   ├── test_validators.py
│   └── test_category_service.py
├── main.py (Application entry point)
├── database.py (DB config placeholder)
├── requirements.txt
└── conftest.py (Pytest config)
```

## Next Steps

1. **SQL Implementation**: Implement `CategoryDAOSQL` with SQLAlchemy
2. **Product Module**: Build Product domain with category integration
3. **Order Module**: Implement Order and OrderLine domains
4. **Invoice Module**: Add Invoice domain
5. **Frontend Enhancements**: Add more UI features (pagination, sorting, bulk operations)
6. **API Layer**: Add REST API using FastAPI
7. **Authentication**: Add user authentication and authorization

## Error Handling

The system uses custom exceptions:
- `ValueError`: For business logic violations (duplicate names, invalid data)
- Pydantic `ValidationError`: For request validation failures
- All errors are caught and displayed to user in UI

## Performance Considerations

- Search is case-insensitive partial match
- Categories sorted by name for consistent ordering
- In-memory mock DAO for testing
- Ready for database indexing on name field
