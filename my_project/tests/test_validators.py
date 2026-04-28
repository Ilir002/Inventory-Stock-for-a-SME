"""Unit tests for Category validators and schemas."""

import pytest
from pydantic import ValidationError
from models.validators import (
    CategorySchema,
    CategoryCreateRequest,
    CategoryUpdateRequest,
)


class TestCategoryCreateRequest:
    """Test CategoryCreateRequest validation."""

    def test_valid_request(self) -> None:
        """Test valid creation request."""
        request = CategoryCreateRequest(name="Electronics", taxes=19.0)
        assert request.name == "Electronics"
        assert request.taxes == 19.0

    def test_name_stripped(self) -> None:
        """Test that name is stripped of whitespace."""
        request = CategoryCreateRequest(name="  Electronics  ", taxes=0.0)
        assert request.name == "Electronics"

    def test_name_too_short(self) -> None:
        """Test validation of short names."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreateRequest(name="A", taxes=0.0)
        assert "at least 2 characters" in str(exc_info.value)

    def test_name_empty(self) -> None:
        """Test validation of empty names."""
        with pytest.raises(ValidationError):
            CategoryCreateRequest(name="", taxes=0.0)

    def test_name_whitespace_only(self) -> None:
        """Test validation of whitespace-only names."""
        with pytest.raises(ValidationError):
            CategoryCreateRequest(name="   ", taxes=0.0)

    def test_name_max_length(self) -> None:
        """Test that long names are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreateRequest(name="A" * 101, taxes=0.0)
        assert "100" in str(exc_info.value)

    def test_taxes_negative(self) -> None:
        """Test validation of negative taxes."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreateRequest(name="Electronics", taxes=-1.0)
        assert "between 0" in str(exc_info.value)

    def test_taxes_over_100(self) -> None:
        """Test validation of taxes over 100."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreateRequest(name="Electronics", taxes=101.0)
        assert "100" in str(exc_info.value)

    def test_default_taxes(self) -> None:
        """Test default tax rate."""
        request = CategoryCreateRequest(name="Electronics")
        assert request.taxes == 0.0

    def test_taxes_boundaries(self) -> None:
        """Test tax rate boundaries."""
        request1 = CategoryCreateRequest(name="Test", taxes=0.0)
        assert request1.taxes == 0.0

        request2 = CategoryCreateRequest(name="Test2", taxes=100.0)
        assert request2.taxes == 100.0


class TestCategoryUpdateRequest:
    """Test CategoryUpdateRequest validation."""

    def test_all_none(self) -> None:
        """Test update request with all None."""
        request = CategoryUpdateRequest(name=None, taxes=None)
        assert request.name is None
        assert request.taxes is None

    def test_partial_update_name(self) -> None:
        """Test partial update with name only."""
        request = CategoryUpdateRequest(name="NewName", taxes=None)
        assert request.name == "NewName"
        assert request.taxes is None

    def test_partial_update_taxes(self) -> None:
        """Test partial update with taxes only."""
        request = CategoryUpdateRequest(name=None, taxes=25.0)
        assert request.name is None
        assert request.taxes == 25.0

    def test_name_validation(self) -> None:
        """Test name validation in update request."""
        with pytest.raises(ValidationError):
            CategoryUpdateRequest(name="A", taxes=None)

    def test_taxes_validation(self) -> None:
        """Test taxes validation in update request."""
        with pytest.raises(ValidationError):
            CategoryUpdateRequest(name=None, taxes=150.0)

    def test_name_stripped(self) -> None:
        """Test that name is stripped."""
        request = CategoryUpdateRequest(name="  NewName  ", taxes=None)
        assert request.name == "NewName"


class TestCategorySchema:
    """Test CategorySchema validation."""

    def test_schema_from_dict(self) -> None:
        """Test creating schema from dictionary."""
        data = {
            "category_id": 1,
            "name": "Electronics",
            "taxes": 19.0,
            "product_count": 5,
        }
        schema = CategorySchema(**data)
        assert schema.category_id == 1
        assert schema.name == "Electronics"
        assert schema.taxes == 19.0
        assert schema.product_count == 5

    def test_schema_validation(self) -> None:
        """Test schema validation."""
        with pytest.raises(ValidationError):
            CategorySchema(
                category_id=1,
                name="A",  # Too short
                taxes=19.0,
            )

    def test_schema_optional_fields(self) -> None:
        """Test optional fields in schema."""
        schema = CategorySchema(
            name="Electronics",
            taxes=19.0,
        )
        assert schema.category_id is None
        assert schema.product_count is None
        assert schema.created_at is None
        assert schema.updated_at is None
