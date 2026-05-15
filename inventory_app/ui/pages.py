from nicegui import ui
from inventory_app.data_access.dao import CategoryDAO, ProductDAO, OrderDAO


@ui.page("/")
def dashboard_page() -> None:

    with ui.header().classes("bg-primary text-white items-center"):
        ui.label("Stefanelli Inventory").classes("text-h6")

    with ui.left_drawer(value=True).classes("bg-grey-2"):
        ui.label("Navigation").classes("text-bold q-pa-md")
        ui.link("Dashboard", "/").classes("block q-pa-sm")
        ui.link("Categories", "/categories").classes("block q-pa-sm")
        ui.link("Products", "/products").classes("block q-pa-sm")
        ui.link("Orders", "/orders").classes("block q-pa-sm")

    with ui.column().classes("w-full q-pa-md"):
        categories = CategoryDAO.list_all()
        products = ProductDAO.list_all()
        low_stock = ProductDAO.list_below_minimum()

        with ui.grid(columns=3).classes("gap-4"):
            with ui.card():
                ui.label("Categories")
                ui.label(str(len(categories))).classes("text-h4")
            with ui.card():
                ui.label("Products")
                ui.label(str(len(products))).classes("text-h4")
            with ui.card():
                ui.label("Below minimum stock")
                colour = "text-negative" if low_stock else "text-positive"
                ui.label(str(len(low_stock))).classes(f"text-h4 {colour}")

        if low_stock:
            ui.separator().classes("q-my-md")
            ui.label("Low-stock items").classes("text-h6")
            rows = [{"name": p.name, "stock": p.current_stock, "min": p.minimum_stock} for p in low_stock]
            ui.table(
                columns=[
                    {"name": "name", "label": "Product", "field": "name", "align": "left"},
                    {"name": "stock", "label": "Current stock", "field": "stock"},
                    {"name": "min", "label": "Minimum", "field": "min"},
                ],
                rows=rows,
            ).classes("w-full")