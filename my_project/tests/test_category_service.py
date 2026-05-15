"""Unit tests for CategoryService."""

import pytest
from typing import List, Optional
from models.category import Category
from models.validators import CategoryCreateRequest, CategoryUpdateRequest, CategorySchema
from services.category_service import CategoryService
from dao.base import ICategoryDAO
from datetime import datetime


class MockCategoryDAO(ICategoryDAO):
    """Mock implementation of ICategoryDAO for testing."""

    def __init__(self):
        """Initialize mock DAO with seeded categories for development."""
        self._categories: dict[int, Category] = {}
        self._next_id = 1

        # Seed categories PASTA and WINE with 10 products each for UI preview
        pasta = Category(
            category_id=self._next_id,
            name="PASTA",
            taxes=10.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        # simulate 10 products
        pasta.products = [None] * 10
        self._categories[self._next_id] = pasta
        self._next_id += 1

        wine = Category(
            category_id=self._next_id,
            name="WINE",
            taxes=20.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        wine.products = [None] * 10
        self._categories[self._next_id] = wine
        self._next_id += 1

    def create(self, request: CategoryCreateRequest) -> Category:
        """Create a new category."""
        category = Category(
            category_id=self._next_id,
            name=request.name,
            taxes=request.taxes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self._categories[self._next_id] = category
        self._next_id += 1
        return category

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        return self._categories.get(category_id)

    def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name."""
        for cat in self._categories.values():
            if cat.name == name:
                return cat
        return None

    def get_all(self) -> List[Category]:
        """Get all categories."""
        return sorted(self._categories.values(), key=lambda x: x.name)

    def update(self, category_id: int, request: CategoryUpdateRequest) -> Optional[Category]:
        """Update a category."""
        category = self._categories.get(category_id)
        if not category:
            return None

        if request.name is not None:
            category.name = request.name
        if request.taxes is not None:
            category.taxes = request.taxes

        category.updated_at = datetime.utcnow()
        return category

    def delete(self, category_id: int) -> bool:
        """Delete a category."""
        if category_id in self._categories:
            # Check if category has products (in mock, we assume no products)
            del self._categories[category_id]
            return True
        return False

    def exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if category name exists."""
        for cat in self._categories.values():
            if cat.name == name:
                if exclude_id is None or cat.category_id != exclude_id:
                    return True
        return False


@pytest.fixture
def service() -> CategoryService:
    """Fixture providing CategoryService with mock DAO."""
    dao = MockCategoryDAO()
    return CategoryService(dao)


class TestCategoryServiceCreate:
    """Test category creation."""

    def test_create_category(self, service: CategoryService) -> None:
        """Test creating a category."""
        result = service.create_category("Electronics", 19.0)
        
        assert result.name == "Electronics"
        assert result.taxes == 19.0
        assert result.category_id is not None

    def test_create_category_default_taxes(self, service: CategoryService) -> None:
        """Test creating category with default taxes."""
        result = service.create_category("Furniture")
        
        assert result.name == "Furniture"
        assert result.taxes == 0.0

    def test_create_duplicate_name(self, service: CategoryService) -> None:
        """Test that duplicate names are rejected."""
        service.create_category("Electronics", 19.0)
        
        with pytest.raises(ValueError) as exc_info:
            service.create_category("Electronics", 10.0)
        assert "already exists" in str(exc_info.value)

    def test_create_invalid_name(self, service: CategoryService) -> None:
        """Test that invalid names are rejected."""
        with pytest.raises(ValueError):
            service.create_category("A")

    def test_create_invalid_taxes(self, service: CategoryService) -> None:
        """Test that invalid taxes are rejected."""
        with pytest.raises(ValueError):
            service.create_category("Electronics", 150.0)


class TestCategoryServiceRead:
    """Test reading categories."""

    def test_get_category_by_id(self, service: CategoryService) -> None:
        """Test getting category by ID."""
        created = service.create_category("Electronics", 19.0)
        result = service.get_category(created.category_id)
        
        assert result is not None
        assert result.name == "Electronics"
        assert result.taxes == 19.0

    def test_get_nonexistent_category(self, service: CategoryService) -> None:
        """Test getting nonexistent category."""
        result = service.get_category(999)
        assert result is None

    def test_get_all_categories(self, service: CategoryService) -> None:
        """Test getting all categories."""
        service.create_category("Electronics", 19.0)
        service.create_category("Furniture", 5.0)
        service.create_category("Clothing", 7.0)
        
        result = service.get_all_categories()
        assert len(result) == 3
        # Should be sorted by name
        assert result[0].name == "Clothing"
        assert result[1].name == "Electronics"
        assert result[2].name == "Furniture"

    def test_get_all_empty(self, service: CategoryService) -> None:
        """Test getting all categories when empty."""
        result = service.get_all_categories()
        assert len(result) == 0


class TestCategoryServiceUpdate:
    """Test updating categories."""

    def test_update_name(self, service: CategoryService) -> None:
        """Test updating category name."""
        created = service.create_category("Electronics", 19.0)
        result = service.update_category(created.category_id, name="Tech Products")
        
        assert result is not None
        assert result.name == "Tech Products"
        assert result.taxes == 19.0

    def test_update_taxes(self, service: CategoryService) -> None:
        """Test updating category taxes."""
        created = service.create_category("Electronics", 19.0)
        result = service.update_category(created.category_id, taxes=21.0)
        
        assert result is not None
        assert result.name == "Electronics"
        assert result.taxes == 21.0

    def test_update_both(self, service: CategoryService) -> None:
        """Test updating both name and taxes."""
        created = service.create_category("Electronics", 19.0)
        result = service.update_category(
            created.category_id,
            name="Tech Products",
            taxes=21.0
        )
        
        assert result is not None
        assert result.name == "Tech Products"
        assert result.taxes == 21.0

    def test_update_nonexistent(self, service: CategoryService) -> None:
        """Test updating nonexistent category."""
        result = service.update_category(999, name="Test")
        assert result is None

    def test_update_duplicate_name(self, service: CategoryService) -> None:
        """Test that duplicate names are rejected on update."""
        cat1 = service.create_category("Electronics", 19.0)
        service.create_category("Furniture", 5.0)
        
        with pytest.raises(ValueError) as exc_info:
            service.update_category(cat1.category_id, name="Furniture")
        assert "already exists" in str(exc_info.value)

    def test_update_same_name(self, service: CategoryService) -> None:
        """Test that updating to same name is allowed."""
        cat = service.create_category("Electronics", 19.0)
        result = service.update_category(cat.category_id, name="Electronics")
        
        assert result is not None
        assert result.name == "Electronics"


class TestCategoryServiceDelete:
    """Test deleting categories."""

    def test_delete_category(self, service: CategoryService) -> None:
        """Test deleting a category."""
        created = service.create_category("Electronics", 19.0)
        result = service.delete_category(created.category_id)
        
        assert result is True
        assert service.get_category(created.category_id) is None

    def test_delete_nonexistent(self, service: CategoryService) -> None:
        """Test deleting nonexistent category."""
        result = service.delete_category(999)
        assert result is False


class TestCategoryServiceSearch:
    """Test searching categories."""

    def test_search_by_name(self, service: CategoryService) -> None:
        """Test searching categories by name."""
        service.create_category("Electronics", 19.0)
        service.create_category("Electronic Accessories", 19.0)
        service.create_category("Furniture", 5.0)
        
        result = service.search_categories("Electronic")
        assert len(result) == 2
        assert all("Electronic" in cat.name for cat in result)

    def test_search_case_insensitive(self, service: CategoryService) -> None:
        """Test that search is case-insensitive."""
        service.create_category("Electronics", 19.0)
        
        result = service.search_categories("electronics")
        assert len(result) == 1
        assert result[0].name == "Electronics"

    def test_search_no_results(self, service: CategoryService) -> None:
        """Test search with no results."""
        service.create_category("Electronics", 19.0)
        
        result = service.search_categories("Furniture")
        assert len(result) == 0

    def test_search_empty(self, service: CategoryService) -> None:
        """Test search with empty query."""
        service.create_category("Electronics", 19.0)
        service.create_category("Furniture", 5.0)
        
        result = service.search_categories("")
        # Empty search should return all
        assert len(result) == 2


class TestCategoryServiceFilters:
    """Test category filtering methods."""

    def test_get_categories_with_products(self, service: CategoryService) -> None:
        """Test getting categories with products."""
        # This test demonstrates the method exists
        # In a real scenario with products, this would filter accordingly
        service.create_category("Electronics", 19.0)
        service.create_category("Furniture", 5.0)
        
        result = service.get_categories_with_products()
        # Without actual products, this should be empty
        assert len(result) == 0

    def test_get_categories_without_products(self, service: CategoryService) -> None:
        """Test getting categories without products."""
        service.create_category("Electronics", 19.0)
        service.create_category("Furniture", 5.0)
        
        result = service.get_categories_without_products()
        # All categories should have no products initially
        assert len(result) == 2
