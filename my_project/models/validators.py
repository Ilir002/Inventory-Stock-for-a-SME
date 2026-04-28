"""Validation schemas for models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _normalize_category_name(value: str) -> str:
    """Normalize a category name before validation."""
    normalized = value.strip()
    if not normalized:
        raise ValueError("Category name cannot be empty")
    if len(normalized) < 2:
        raise ValueError("Category name must be at least 2 characters")
    return normalized


class CategorySchema(BaseModel):
    """Pydantic schema for Category."""

    model_config = ConfigDict(from_attributes=True)

    category_id: Optional[int] = None
    name: str = Field(..., max_length=100)
    taxes: float = Field(..., ge=0.0, le=100.0)
    product_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate category name."""
        return _normalize_category_name(v)

    @field_validator("taxes")
    @classmethod
    def validate_taxes(cls, v: float) -> float:
        """Validate tax percentage."""
        if v < 0 or v > 100:
            raise ValueError("Tax percentage must be between 0 and 100")
        return round(v, 2)

class CategoryCreateRequest(BaseModel):
    """Request schema for creating a category."""

    name: str = Field(..., max_length=100)
    taxes: float = Field(default=0.0, ge=0.0, le=100.0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate category name."""
        return _normalize_category_name(v)


class CategoryUpdateRequest(BaseModel):
    """Request schema for updating a category."""

    name: Optional[str] = Field(None, max_length=100)
    taxes: Optional[float] = Field(None, ge=0.0, le=100.0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate category name."""
        if v is not None:
            return _normalize_category_name(v)
        return v
