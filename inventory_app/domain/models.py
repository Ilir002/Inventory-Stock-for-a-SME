from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    category_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    taxes: float = Field(default=0.0)

    products: List["Product"] = Relationship(back_populates="category")  # 1 to many

    @property
    def product_count(self) -> int:
        return len(self.products)  # derived attribute


class Product(SQLModel, table=True):
    __tablename__ = "products"

    product_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    barcode: Optional[str] = Field(default=None, unique=True)
    price: float = Field(default=0.0)
    purchase_cost: float = Field(default=0.0)
    minimum_stock: int = Field(default=0)
    optimal_stock: int = Field(default=0)

    category_id: int = Field(foreign_key="categories.category_id")  # many to one
    category: Optional["Category"] = Relationship(back_populates="products")
    order_lines: List["OrderLine"] = Relationship(back_populates="product")  # 1 to many

    @property
    def current_stock(self) -> int:
        return sum(line.quantity_change for line in self.order_lines)  # derived attribute

    @property
    def is_below_minimum(self) -> bool:
        return self.current_stock < self.minimum_stock  # derived attribute


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow)
    movement_type: str = Field(default="inbound")  # inbound, sale, waste
    status: str = Field(default="draft")

    order_lines: List["OrderLine"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )  # 1 to many
    invoice: Optional["Invoice"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "uselist": False},
    )  # 1 to 1

    @property
    def total_amount(self) -> float:
        return sum(abs(line.quantity_change) * line.unit_price for line in self.order_lines)  # derived attribute


class OrderLine(SQLModel, table=True):
    __tablename__ = "order_lines"

    order_line_id: Optional[int] = Field(default=None, primary_key=True)
    quantity_change: int = Field()  # positiv = Eingang, negativ = Ausgang
    unit_price: float = Field(default=0.0)

    order_id: int = Field(foreign_key="orders.order_id")  # many to one
    order: Optional["Order"] = Relationship(back_populates="order_lines")
    product_id: int = Field(foreign_key="products.product_id")  # many to one
    product: Optional["Product"] = Relationship(back_populates="order_lines")


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    invoice_id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow)
    document_path: str = Field()

    order_id: int = Field(foreign_key="orders.order_id", unique=True)  # 1 to 1
    order: Optional["Order"] = Relationship(back_populates="invoice")