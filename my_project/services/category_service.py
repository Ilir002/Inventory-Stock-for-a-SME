"""Category service with business logic."""

from typing import List, Optional
from dao.base import ICategoryDAO
from models.validators import CategorySchema, CategoryCreateRequest, CategoryUpdateRequest
from models.category import Category


class CategoryService:
    """Service layer for Category - handles business logic and validation."""

    def __init__(self, dao: ICategoryDAO):
        """
        Initialize service with DAO.
        
        Args:
            dao: Implementation of ICategoryDAO (can be SQL or in-memory)
        """
        self.dao = dao

    def create_category(self, name: str, taxes: float = 0.0) -> CategorySchema:
        """
        Create a new category with validation.
        
        Args:
            name: Category name
            taxes: Tax rate (0-100)
            
        Returns:
            CategorySchema with created category data
            
        Raises:
            ValueError: If validation fails or name already exists
        """
        # Create and validate request
        request = CategoryCreateRequest(name=name, taxes=taxes)
        
        # Check if name already exists
        if self.dao.exists(request.name):
            raise ValueError(f"Category '{request.name}' already exists")
        
        # Create category
        category = self.dao.create(request)
        return self._to_schema(category)

    def get_category(self, category_id: int) -> Optional[CategorySchema]:
        """
        Get a category by ID.
        
        Args:
            category_id: The category ID
            
        Returns:
            CategorySchema or None if not found
        """
        category = self.dao.get_by_id(category_id)
        return self._to_schema(category) if category else None

    def get_all_categories(self) -> List[CategorySchema]:
        """
        Get all categories sorted by name.
        
        Returns:
            List of CategorySchema objects
        """
        categories = self.dao.get_all()
        return [self._to_schema(cat) for cat in categories]

    def update_category(self, category_id: int, name: Optional[str] = None, taxes: Optional[float] = None) -> Optional[CategorySchema]:
        """
        Update a category with validation.
        
        Args:
            category_id: The category ID
            name: New category name (optional)
            taxes: New tax rate (optional)
            
        Returns:
            Updated CategorySchema or None if not found
            
        Raises:
            ValueError: If validation fails or name already exists
        """
        category = self.dao.get_by_id(category_id)
        if not category:
            return None

        # If name is being updated, check for duplicates
        if name is not None and name != category.name:
            if self.dao.exists(name):
                raise ValueError(f"Category '{name}' already exists")

        # Create and validate request
        request = CategoryUpdateRequest(name=name, taxes=taxes)
        
        # Update category
        updated = self.dao.update(category_id, request)
        return self._to_schema(updated) if updated else None

    def delete_category(self, category_id: int) -> bool:
        """
        Delete a category.
        
        Args:
            category_id: The category ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If category has products
        """
        return self.dao.delete(category_id)

    def search_categories(self, query: str) -> List[CategorySchema]:
        """
        Search categories by name (case-insensitive partial match).
        
        Args:
            query: Search query
            
        Returns:
            List of matching CategorySchema objects
        """
        all_categories = self.dao.get_all()
        query_lower = query.lower()
        filtered = [
            cat for cat in all_categories 
            if query_lower in cat.name.lower()
        ]
        return [self._to_schema(cat) for cat in filtered]

    def get_categories_with_products(self) -> List[CategorySchema]:
        """
        Get categories that have at least one product.
        
        Returns:
            List of CategorySchema objects with products
        """
        all_categories = self.dao.get_all()
        filtered = [cat for cat in all_categories if cat.product_count > 0]
        return [self._to_schema(cat) for cat in filtered]

    def get_categories_without_products(self) -> List[CategorySchema]:
        """
        Get categories that have no products.
        
        Returns:
            List of CategorySchema objects without products
        """
        all_categories = self.dao.get_all()
        filtered = [cat for cat in all_categories if cat.product_count == 0]
        return [self._to_schema(cat) for cat in filtered]

    @staticmethod
    def _to_schema(category: Optional[Category]) -> Optional[CategorySchema]:
        """Convert Category to CategorySchema."""
        if category is None:
            return None
        return CategorySchema.model_validate(category)
