"""Abstract base DAO interface for Category."""

from abc import ABC, abstractmethod
from typing import List, Optional
from models.category import Category
from models.validators import CategoryCreateRequest, CategoryUpdateRequest


class ICategoryDAO(ABC):
    """Abstract interface for Category data access."""

    @abstractmethod
    def create(self, request: CategoryCreateRequest) -> Category:
        """Create a new category."""
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name."""
        pass

    @abstractmethod
    def get_all(self) -> List[Category]:
        """Get all categories."""
        pass

    @abstractmethod
    def update(self, category_id: int, request: CategoryUpdateRequest) -> Optional[Category]:
        """Update a category."""
        pass

    @abstractmethod
    def delete(self, category_id: int) -> bool:
        """Delete a category."""
        pass

    @abstractmethod
    def exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if category name exists."""
        pass
