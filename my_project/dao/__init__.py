"""DAO package - Data Access Objects."""

from .base import ICategoryDAO
from .category_dao import CategoryDAO

__all__ = ["ICategoryDAO", "CategoryDAO"]
