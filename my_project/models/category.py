"""Category model."""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Category(Base):
    """Category ORM model representing product categories."""

    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    taxes = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to Product (one-to-many)
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Category(id={self.category_id}, name='{self.name}', taxes={self.taxes}%)"

    @property
    def product_count(self) -> int:
        """Get count of products in this category."""
        return len(self.products) if self.products else 0

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "category_id": self.category_id,
            "name": self.name,
            "taxes": self.taxes,
            "product_count": self.product_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
