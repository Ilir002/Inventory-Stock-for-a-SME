from inventory_app.data_access.db import Database
from inventory_app.domain.models import Category, Product, Order, OrderLine, Invoice
from sqlmodel import select


PASTA_PRODUCTS = [
    {"name": "Conchiglioni Pasta Panarese 500g", "barcode": "8032692902005", "price": 12.0, "purchase_cost": 3.5, "minimum_stock": 2, "optimal_stock": 6, "initial_stock": 1},
    {"name": "Gigli pasta Panarese 500g", "barcode": "8032692902029", "price": 12.0, "purchase_cost": 3.5, "minimum_stock": 3, "optimal_stock": 8, "initial_stock": 5},
    {"name": "Pappardelle Pasta Panarese 500g", "barcode": "8032692902111", "price": 12.0, "purchase_cost": 3.5, "minimum_stock": 3, "optimal_stock": 6, "initial_stock": 12},
    {"name": "Pici Pasta Panarese 500g", "barcode": "8009167012095", "price": 12.0, "purchase_cost": 3.5, "minimum_stock": 3, "optimal_stock": 5, "initial_stock": 8},
    {"name": "Fusilloni Panarese 500g", "barcode": "8032692902012", "price": 12.0, "purchase_cost": 3.5, "minimum_stock": 3, "optimal_stock": 10, "initial_stock": 10},
    {"name": "Colonne Pompei Fabbrica della Pasta 500g", "barcode": "8033406265775", "price": 12.0, "purchase_cost": 4.0, "minimum_stock": 5, "optimal_stock": 10, "initial_stock": 3},
    {"name": "Fusilli Capri 500g", "barcode": "8033406265850", "price": 12.0, "purchase_cost": 4.0, "minimum_stock": 3, "optimal_stock": 8, "initial_stock": 0},
    {"name": "Candele di Martino 500g", "barcode": "8002459901527", "price": 12.0, "purchase_cost": 4.2, "minimum_stock": 2, "optimal_stock": 6, "initial_stock": 2},
    {"name": "Riccioli Barolo Alfieri 250g", "barcode": "8031175059908", "price": 12.5, "purchase_cost": 5.0, "minimum_stock": 3, "optimal_stock": 8, "initial_stock": 8},
    {"name": "Tortelloni Alfieri spinaci 500g", "barcode": "8031175020502", "price": 13.9, "purchase_cost": 5.5, "minimum_stock": 5, "optimal_stock": 15, "initial_stock": 18},
]

WINE_PRODUCTS = [
    {"name": "Barolo Borgogno 2018", "barcode": "8014560100145", "price": 45.0, "purchase_cost": 28.0, "minimum_stock": 3, "optimal_stock": 10, "initial_stock": 8},
    {"name": "Chianti Classico Riserva 2019", "barcode": "8032802310012", "price": 32.0, "purchase_cost": 18.0, "minimum_stock": 3, "optimal_stock": 8, "initial_stock": 5},
    {"name": "Amarone della Valpolicella 2017", "barcode": "8004300100234", "price": 58.0, "purchase_cost": 35.0, "minimum_stock": 2, "optimal_stock": 6, "initial_stock": 4},
    {"name": "Brunello di Montalcino 2016", "barcode": "8012345678901", "price": 75.0, "purchase_cost": 48.0, "minimum_stock": 2, "optimal_stock": 5, "initial_stock": 0},
    {"name": "Prosecco Valdobbiadene DOCG", "barcode": "8023000100456", "price": 18.0, "purchase_cost": 9.0, "minimum_stock": 5, "optimal_stock": 15, "initial_stock": 12},
    {"name": "Pinot Grigio Alto Adige 2022", "barcode": "8034500200123", "price": 22.0, "purchase_cost": 12.0, "minimum_stock": 4, "optimal_stock": 10, "initial_stock": 7},
    {"name": "Soave Classico Pieropan 2021", "barcode": "8045600300234", "price": 19.0, "purchase_cost": 10.0, "minimum_stock": 3, "optimal_stock": 8, "initial_stock": 0},
    {"name": "Grappa di Barolo Marchesi", "barcode": "8056700400345", "price": 42.0, "purchase_cost": 25.0, "minimum_stock": 2, "optimal_stock": 6, "initial_stock": 3},
    {"name": "Franciacorta Brut DOCG", "barcode": "8067800500456", "price": 28.0, "purchase_cost": 15.0, "minimum_stock": 4, "optimal_stock": 10, "initial_stock": 6},
    {"name": "Vino Nobile di Montepulciano 2018", "barcode": "8078900600567", "price": 35.0, "purchase_cost": 20.0, "minimum_stock": 3, "optimal_stock": 8, "initial_stock": 0},
]


def seed_if_empty() -> None:
    with Database.session() as session:
        # nur seeden wenn DB leer ist
        if session.exec(select(Category)).first() is not None:
            return

        # Kategorien erstellen
        pasta_cat = Category(name="PASTA", taxes=0.026)
        wine_cat = Category(name="WINE", taxes=0.077)
        session.add(pasta_cat)
        session.add(wine_cat)
        session.flush()

        # Produkte erstellen
        all_products = []
        for spec in PASTA_PRODUCTS:
            p = Product(
                name=spec["name"],
                barcode=spec["barcode"],
                price=spec["price"],
                purchase_cost=spec["purchase_cost"],
                minimum_stock=spec["minimum_stock"],
                optimal_stock=spec["optimal_stock"],
                category_id=pasta_cat.category_id,
            )
            session.add(p)
            all_products.append((p, spec["initial_stock"]))

        for spec in WINE_PRODUCTS:
            p = Product(
                name=spec["name"],
                barcode=spec["barcode"],
                price=spec["price"],
                purchase_cost=spec["purchase_cost"],
                minimum_stock=spec["minimum_stock"],
                optimal_stock=spec["optimal_stock"],
                category_id=wine_cat.category_id,
            )
            session.add(p)
            all_products.append((p, spec["initial_stock"]))

        session.flush()

        # Startbestand als INBOUND Order speichern
        initial_order = Order(movement_type="inbound", status="confirmed")
        session.add(initial_order)
        session.flush()

        for product, qty in all_products:
            if qty > 0:
                line = OrderLine(
                    order_id=initial_order.order_id,
                    product_id=product.product_id,
                    quantity_change=qty,
                    unit_price=product.purchase_cost,
                )
                session.add(line)