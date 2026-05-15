import pytest
from sqlalchemy.exc import IntegrityError
from inventory_app.domain.models import Category, Product, Order, OrderLine
from inventory_app.data_access.dao import CategoryDAO, ProductDAO, OrderDAO
from inventory_app.data_access.seed import seed_if_empty


# ─── Unit Tests ───────────────────────────────────────────────────────────────

def test_current_stock_berechnung():
    # Arrange
    product = Product(name="Test", price=10.0, purchase_cost=5.0,
                      minimum_stock=3, optimal_stock=10, category_id=1)
    product.order_lines = [
        OrderLine(quantity_change=10, unit_price=5.0, order_id=1, product_id=1),
        OrderLine(quantity_change=-3, unit_price=10.0, order_id=1, product_id=1),
    ]
    # Act & Assert
    assert product.current_stock == 7  # derived attribute


def test_low_stock_alert_aktiv():
    # Arrange
    product = Product(name="Test", price=10.0, purchase_cost=5.0,
                      minimum_stock=5, optimal_stock=10, category_id=1)
    product.order_lines = [
        OrderLine(quantity_change=2, unit_price=5.0, order_id=1, product_id=1),
    ]
    # Act & Assert
    assert product.is_below_minimum is True  # 2 < 5


def test_low_stock_alert_nicht_aktiv():
    # Arrange
    product = Product(name="Test", price=10.0, purchase_cost=5.0,
                      minimum_stock=5, optimal_stock=10, category_id=1)
    product.order_lines = [
        OrderLine(quantity_change=5, unit_price=5.0, order_id=1, product_id=1),
    ]
    # Act & Assert
    assert product.is_below_minimum is False  # 5 == 5, kein Alert


def test_total_amount_berechnung():
    # Arrange
    order = Order(movement_type="inbound", status="confirmed")
    order.order_lines = [
        OrderLine(quantity_change=3, unit_price=4.0, order_id=1, product_id=1),
        OrderLine(quantity_change=2, unit_price=8.0, order_id=1, product_id=2),
    ]
    # Act & Assert
    assert order.total_amount == 28.0  # 3*4 + 2*8 = 28


# ─── DB Tests ─────────────────────────────────────────────────────────────────

def test_seed_erstellt_categories_und_products():
    # Arrange & Act
    seed_if_empty()
    # Assert
    cats = CategoryDAO.list_all()
    prods = ProductDAO.list_all()
    assert {c.name for c in cats} == {"PASTA", "WINE"}
    assert len(prods) == 20


def test_leere_db_gibt_leere_liste():
    # Arrange - DB ist leer (conftest macht das automatisch)
    # Act
    cats = CategoryDAO.list_all()
    prods = ProductDAO.list_all()
    # Assert
    assert cats == []
    assert prods == []


def test_category_speichern():
    # Arrange
    cat = Category(name="TEST", taxes=0.026)
    # Act
    saved = CategoryDAO.save(cat)
    # Assert
    assert saved.category_id is not None  # ID wurde automatisch vergeben
    assert saved.name == "TEST"