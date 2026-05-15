from typing import List, Optional
from sqlalchemy.orm import selectinload
from sqlmodel import select
from inventory_app.data_access.db import Database
from inventory_app.domain.models import Category, Product, Order, Invoice


class CategoryDAO:

    @staticmethod
    def list_all() -> List[Category]:
        with Database.session() as session:
            statement = select(Category).options(selectinload(Category.products))
            return list(session.exec(statement).all())

    @staticmethod
    def get(category_id: int) -> Optional[Category]:
        with Database.session() as session:
            statement = select(Category).where(Category.category_id == category_id).options(selectinload(Category.products))
            return session.exec(statement).first()

    @staticmethod
    def save(category: Category) -> Category:
        with Database.session() as session:
            session.add(category)
            session.commit()
            session.refresh(category, ["products"])
            return category

    @staticmethod
    def delete(category_id: int) -> bool:
        with Database.session() as session:
            obj = session.get(Category, category_id)
            if obj is None:
                return False
            session.delete(obj)
            return True


class ProductDAO:

    @staticmethod
    def list_all() -> List[Product]:
        with Database.session() as session:
            statement = select(Product).options(
                selectinload(Product.order_lines),
                selectinload(Product.category),
            )
            return list(session.exec(statement).all())

    @staticmethod
    def get(product_id: int) -> Optional[Product]:
        with Database.session() as session:
            statement = select(Product).where(Product.product_id == product_id).options(
                selectinload(Product.order_lines),
                selectinload(Product.category),
            )
            return session.exec(statement).first()

    @staticmethod
    def get_by_barcode(barcode: str) -> Optional[Product]:
        with Database.session() as session:
            statement = select(Product).where(Product.barcode == barcode).options(
                selectinload(Product.order_lines),
                selectinload(Product.category),
            )
            return session.exec(statement).first()

    @staticmethod
    def list_below_minimum() -> List[Product]:
        return [p for p in ProductDAO.list_all() if p.is_below_minimum]

    @staticmethod
    def save(product: Product) -> Product:
        with Database.session() as session:
            session.add(product)
            session.commit()
            session.refresh(product, ["order_lines", "category"])
            return product

    @staticmethod
    def delete(product_id: int) -> bool:
        with Database.session() as session:
            obj = session.get(Product, product_id)
            if obj is None:
                return False
            session.delete(obj)
            return True


class OrderDAO:

    @staticmethod
    def list_all() -> List[Order]:
        with Database.session() as session:
            statement = select(Order).options(
                selectinload(Order.order_lines),
                selectinload(Order.invoice),
            )
            return list(session.exec(statement).all())

    @staticmethod
    def get(order_id: int) -> Optional[Order]:
        with Database.session() as session:
            statement = select(Order).where(Order.order_id == order_id).options(
                selectinload(Order.order_lines),
                selectinload(Order.invoice),
            )
            return session.exec(statement).first()

    @staticmethod
    def save(order: Order) -> Order:
        with Database.session() as session:
            session.add(order)
            session.commit()
            session.refresh(order, ["order_lines", "invoice"])
            return order


class InvoiceDAO:

    @staticmethod
    def list_all() -> List[Invoice]:
        with Database.session() as session:
            statement = select(Invoice)
            return list(session.exec(statement).all())

    @staticmethod
    def save(invoice: Invoice) -> Invoice:
        with Database.session() as session:
            session.add(invoice)
            session.commit()
            session.refresh(invoice)
            return invoice