"""Validation schemas for models."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class CategorySchema(BaseModel):
    """Pydantic schema for Category."""

    category_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    taxes: float = Field(..., ge=0.0, le=100.0)
    product_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate category name."""
        # Remove leading/trailing whitespace
        v = v.strip()
        if not v:
            raise ValueError("Category name cannot be empty")
        if len(v) < 2:
            raise ValueError("Category name must be at least 2 characters")
        return v

    @field_validator("taxes")
    @classmethod
    def validate_taxes(cls, v: float) -> float:
        """Validate tax percentage."""
        if v < 0 or v > 100:
            raise ValueError("Tax percentage must be between 0 and 100")
        return round(v, 2)

    class Config:
        """Pydantic config."""
        from_attributes = True


class CategoryCreateRequest(BaseModel):
    """Request schema for creating a category."""

    name: str = Field(..., min_length=2, max_length=100)
    taxes: float = Field(default=0.0, ge=0.0, le=100.0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate category name."""
        return v.strip()


class CategoryUpdateRequest(BaseModel):
    """Request schema for updating a category."""

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    taxes: Optional[float] = Field(None, ge=0.0, le=100.0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate category name."""
        if v is not None:
            return v.strip()
        return v
