"""Application entry point."""

from nicegui import ui
from services.category_service import CategoryService
from ui.pages import CategoryPages
from tests.test_category_service import MockCategoryDAO


# Initialize mock DAO (will be replaced with SQL DAO later)
dao = MockCategoryDAO()
category_service = CategoryService(dao)
category_pages = CategoryPages(category_service)


@ui.page("/")
async def home() -> None:
    """Home page."""
    with ui.column().classes("w-full items-center justify-center p-4"):
        ui.label("Inventory Stock Management").classes("text-4xl font-bold")
        ui.label("Category Management System").classes("text-lg text-gray-600")
        
        with ui.row().classes("gap-4 mt-8"):
            ui.button("View Categories", icon="list").on_click(
                lambda: ui.navigate("/categories")
            ).props("outline").classes("px-8 py-3")
            
            ui.button("Add Category", icon="add", color="positive").on_click(
                lambda: ui.navigate("/category/create")
            ).classes("px-8 py-3")


@ui.page("/categories")
async def categories_list() -> None:
    """Categories list page."""
    category_pages.list_page()


@ui.page("/category/create")
async def category_create() -> None:
    """Category creation page."""
    category_pages.create_page()


@ui.page("/category/edit/{category_id}")
async def category_edit(category_id: int) -> None:
    """Category edit page."""
    category_pages.edit_page(category_id)


def main() -> None:
    """Run the application."""
    ui.run(title="Inventory Management", port=8080)


if __name__ == "__main__":
    main()
