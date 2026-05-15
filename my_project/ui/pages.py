"""NiceGUI pages for Category management."""

from nicegui import ui
from services.category_service import CategoryService
from dao.base import ICategoryDAO
from ui.components import CategoryCard, CategoryForm, CategorySelector
from typing import Optional


class CategoryPages:
    """Container for all category management pages."""

    def __init__(self, service: CategoryService):
        """
        Initialize pages with service.
        
        Args:
            service: CategoryService instance
        """
        self.service = service

    def list_page(self) -> None:
        """
        Category list page with search and management options.
        """
        ui.page_title("Categories")
        
        with ui.column().classes("w-full max-w-4xl mx-auto gap-4 p-4"):
            # Header
            with ui.row().classes("w-full items-center justify-between"):
                ui.label("Categories").classes("text-3xl font-bold")
                ui.button("Add Category", icon="add", color="positive").on_click(
                    lambda: ui.navigate.to("/category/create")
                )

            # Categories container
            categories_container = ui.column().classes("w-full gap-2")

            def render_categories(query: str = "") -> None:
                """Render category cards."""
                categories_container.clear()
                
                if query:
                    categories = self.service.search_categories(query)
                else:
                    categories = self.service.get_all_categories()

                if not categories:
                    with categories_container:
                        ui.label("No categories found").classes("text-gray-500 text-center py-8")
                else:
                    with categories_container:
                        for category in categories:
                            with ui.card().classes("w-full"):
                                with ui.row().classes("w-full items-center justify-between"):
                                    with ui.column():
                                        ui.label(category.name).classes("text-base font-bold")
                                        ui.label(f"Tax Rate: {category.taxes}%").classes(
                                            "text-sm text-gray-600"
                                        )
                                        ui.label(f"Products: {category.product_count}").classes(
                                            "text-sm text-blue-600 font-medium"
                                        )

                                    with ui.row():
                                        ui.button(
                                            "Edit",
                                            icon="edit",
                                            color="primary",
                                        ).on_click(
                                            lambda cid=category.category_id: ui.navigate.to(
                                                f"/category/edit/{cid}"
                                            )
                                        ).props("flat")

                                        ui.button(
                                            "Delete",
                                            icon="delete",
                                            color="negative",
                                        ).on_click(
                                            lambda cid=category.category_id: self._show_delete_dialog(cid)
                                        ).props("flat")

            # Initial render
            render_categories()

            # Search input (use on_change param for NiceGUI)
            search_input = ui.input(
                placeholder="Search categories...",
                on_change=lambda e: render_categories(e.value) if e.value else render_categories(),
            ).props("outlined").classes("w-full")

    def create_page(self) -> None:
        """
        Category creation page.
        """
        ui.page_title("Create Category")

        with ui.column().classes("w-full max-w-2xl mx-auto gap-4 p-4"):
            ui.label("Create New Category").classes("text-3xl font-bold")

            name_input = ui.input(
                label="Category Name",
                placeholder="Enter category name",
            ).props("outlined").classes("w-full")

            taxes_input = ui.number(
                label="Tax Rate (%)",
                value=0.0,
                min=0,
                max=100,
            ).props("outlined").classes("w-full")

            message_label = ui.label().classes("text-sm")

            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Cancel", icon="close").on_click(
                    lambda: ui.navigate.to("/categories")
                ).props("outlined")

                async def save_category() -> None:
                    """Save new category."""
                    try:
                        name = name_input.value
                        taxes = taxes_input.value

                        if not name or not name.strip():
                            message_label.text = "❌ Please enter a category name"
                            message_label.classes("text-red-600")
                            return

                        # Create category
                        self.service.create_category(name, taxes)
                        message_label.text = "✓ Category created successfully"
                        message_label.classes("text-green-600")
                        
                        # Navigate after success
                        ui.timer(1.0, lambda: ui.navigate.to("/categories"))

                    except ValueError as e:
                        message_label.text = f"❌ {str(e)}"
                        message_label.classes("text-red-600")
                    except Exception as e:
                        message_label.text = f"❌ Error: {str(e)}"
                        message_label.classes("text-red-600")

                ui.button("Save", icon="check", color="positive").on_click(save_category)

    def edit_page(self, category_id: int) -> None:
        """
        Category edit page.
        
        Args:
            category_id: ID of category to edit
        """
        ui.page_title("Edit Category")

        with ui.column().classes("w-full max-w-2xl mx-auto gap-4 p-4"):
            # Get category
            category = self.service.get_category(category_id)
            
            if not category:
                ui.label("Category not found").classes("text-red-600 text-lg")
                return

            ui.label(f"Edit Category: {category.name}").classes("text-3xl font-bold")

            name_input = ui.input(
                label="Category Name",
                value=category.name,
                placeholder="Enter category name",
            ).props("outlined").classes("w-full")

            taxes_input = ui.number(
                label="Tax Rate (%)",
                value=category.taxes,
                min=0,
                max=100,
            ).props("outlined").classes("w-full")

            message_label = ui.label().classes("text-sm")

            with ui.row().classes("w-full items-center justify-between"):
                ui.label(f"Products in category: {category.product_count}").classes(
                    "text-sm text-blue-600 font-medium"
                )

                with ui.row().classes("gap-2"):
                    ui.button("Cancel", icon="close").on_click(
                        lambda: ui.navigate.to("/categories")
                    ).props("outlined")

                    async def update_category() -> None:
                        """Update category."""
                        try:
                            name = name_input.value
                            taxes = taxes_input.value

                            if not name or not name.strip():
                                message_label.text = "❌ Please enter a category name"
                                message_label.classes("text-red-600")
                                return

                            # Update category
                            self.service.update_category(category_id, name, taxes)
                            message_label.text = "✓ Category updated successfully"
                            message_label.classes("text-green-600")
                            
                            # Navigate after success
                            ui.timer(1.0, lambda: ui.navigate.to("/categories"))

                        except ValueError as e:
                            message_label.text = f"❌ {str(e)}"
                            message_label.classes("text-red-600")
                        except Exception as e:
                            message_label.text = f"❌ Error: {str(e)}"
                            message_label.classes("text-red-600")

                    ui.button("Update", icon="check", color="positive").on_click(update_category)

    def _show_delete_dialog(self, category_id: int) -> None:
        """
        Show delete confirmation dialog.
        
        Args:
            category_id: ID of category to delete
        """
        category = self.service.get_category(category_id)
        if not category:
            return

        with ui.dialog() as dialog:
            with ui.card().classes("gap-4"):
                ui.label(f"Delete '{category.name}'?").classes("text-lg font-bold")
                
                if category.product_count > 0:
                    ui.label(
                        f"⚠️ This category has {category.product_count} product(s). "
                        "Deleting may affect your inventory."
                    ).classes("text-sm text-orange-600")
                else:
                    ui.label("This category will be permanently deleted.").classes("text-sm text-gray-600")

                with ui.row().classes("justify-end gap-2"):
                    ui.button("Cancel", icon="close").on_click(dialog.close).props("outlined")

                    async def confirm_delete() -> None:
                        """Confirm deletion."""
                        try:
                            self.service.delete_category(category_id)
                            dialog.close()
                            ui.notify(f"Category '{category.name}' deleted", type="positive")
                            # Refresh page
                            ui.page.refresh()
                        except ValueError as e:
                            ui.notify(f"❌ {str(e)}", type="negative")
                        except Exception as e:
                            ui.notify(f"❌ Error: {str(e)}", type="negative")

                    ui.button("Delete", icon="delete", color="negative").on_click(confirm_delete)

        dialog.open()


# Top-level NiceGUI page route for categories
@ui.page('/categories')
def categories_route() -> None:
    """
    Route handler for `/categories` that constructs the service and
    delegates rendering to `CategoryPages.list_page()`.
    """
    # Lazy import to avoid circular imports at module import time
    from database import init_db, SessionLocal
    from dao.category_dao import CategoryDAO

    # Ensure DB tables exist (safe to call repeatedly)
    try:
        init_db()
    except Exception:
        # ignore init errors in environments where DB isn't writable
        pass

    # Create a DAO and service instance for the page
    db = SessionLocal()
    dao = CategoryDAO(db)
    service = CategoryService(dao)
    pages = CategoryPages(service)

    # Render the list page
    pages.list_page()
