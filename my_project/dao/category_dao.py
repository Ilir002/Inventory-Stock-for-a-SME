"""Category data access object."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from dao.base import ICategoryDAO
from models.category import Category
from models.validators import CategoryCreateRequest, CategoryUpdateRequest


class CategoryDAO(ICategoryDAO):
    """Data Access Object for Category - handles database operations."""

    def __init__(self, db: Session):
        """Initialize DAO with database session."""
        self.db = db

    def create(self, request: CategoryCreateRequest) -> Category:
        """
        Create a new category.
        
        Args:
            request: CategoryCreateRequest with name and taxes
            
        Returns:
            Created Category instance
            
        Raises:
            ValueError: If category name already exists
        """
        try:
            category = Category(
                name=request.name,
                taxes=request.taxes
            )
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
            return category
        except IntegrityError as e:
            self.db.rollback()
            if "unique constraint" in str(e).lower():
                raise ValueError(f"Category '{request.name}' already exists")
            raise

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """
        Get category by ID.
        
        Args:
            category_id: The category ID
            
        Returns:
            Category instance or None if not found
        """
        return self.db.query(Category).filter(Category.category_id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        """
        Get category by name.
        
        Args:
            name: The category name
            
        Returns:
            Category instance or None if not found
        """
        return self.db.query(Category).filter(Category.name == name).first()

    def get_all(self) -> List[Category]:
        """
        Get all categories.
        
        Returns:
            List of Category instances, sorted by name
        """
        return self.db.query(Category).order_by(Category.name).all()

    def update(self, category_id: int, request: CategoryUpdateRequest) -> Optional[Category]:
        """
        Update a category.
        
        Args:
            category_id: The category ID
            request: CategoryUpdateRequest with updated values
            
        Returns:
            Updated Category instance or None if not found
            
        Raises:
            ValueError: If new name already exists
        """
        category = self.get_by_id(category_id)
        if not category:
            return None

        try:
            if request.name is not None:
                category.name = request.name
            if request.taxes is not None:
                category.taxes = request.taxes

            self.db.commit()
            self.db.refresh(category)
            return category
        except IntegrityError as e:
            self.db.rollback()
            if "unique constraint" in str(e).lower():
                raise ValueError(f"Category name '{request.name}' already exists")
            raise

    def delete(self, category_id: int) -> bool:
        """
        Delete a category.
        
        Args:
            category_id: The category ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If category has products
        """
        category = self.get_by_id(category_id)
        if not category:
            return False

        if category.product_count > 0:
            raise ValueError(
                f"Cannot delete category '{category.name}' with {category.product_count} products"
            )

        self.db.delete(category)
        self.db.commit()
        return True

    def exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if category name exists.
        
        Args:
            name: Category name to check
            exclude_id: Optionally exclude a category ID from check
            
        Returns:
            True if exists, False otherwise
        """
        query = self.db.query(Category).filter(Category.name == name)
        if exclude_id is not None:
            query = query.filter(Category.category_id != exclude_id)
        return query.first() is not None

