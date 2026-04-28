"""Reusable NiceGUI components for Category."""

from nicegui import ui
from typing import Optional, Callable, List
from models.validators import CategorySchema


class CategorySelector:
    """Reusable category selection component."""

    def __init__(
        self,
        categories: List[CategorySchema],
        on_change: Optional[Callable[[int], None]] = None,
        label: str = "Category",
    ):
        """
        Initialize category selector.
        
        Args:
            categories: List of available categories
            on_change: Callback when selection changes
            label: Label for the selector
        """
        self.categories = categories
        self.on_change = on_change
        self.label = label
        self.select = None

    def render(self) -> ui.select:
        """
        Render the selector component.
        
        Returns:
            The NiceGUI select element
        """
        options = {str(cat.category_id): cat.name for cat in self.categories}
        
        self.select = ui.select(
            options,
            label=self.label,
        )
        
        if self.on_change:
            self.select.on_change(
                lambda e: self.on_change(int(e.value)) if e.value else None
            )
        
        return self.select

    def get_value(self) -> Optional[int]:
        """Get selected category ID."""
        if self.select and self.select.value:
            return int(self.select.value)
        return None

    def set_value(self, category_id: int) -> None:
        """Set selected category ID."""
        if self.select:
            self.select.value = str(category_id)


class CategoryForm:
    """Reusable category form component."""

    def __init__(
        self,
        on_submit: Callable[[str, float], None],
        category: Optional[CategorySchema] = None,
        button_label: str = "Save",
    ):
        """
        Initialize category form.
        
        Args:
            on_submit: Callback when form is submitted
            category: Optional category to edit
            button_label: Label for submit button
        """
        self.on_submit = on_submit
        self.category = category
        self.button_label = button_label
        self.name_input = None
        self.taxes_input = None

    def render(self) -> None:
        """Render the form component."""
        with ui.card():
            ui.label("Category Details").classes("text-lg font-bold")
            
            self.name_input = ui.input(
                label="Category Name",
                placeholder="Enter category name",
                value=self.category.name if self.category else "",
            ).props("outlined")
            self.name_input.classes("w-full")

            self.taxes_input = ui.number(
                label="Tax Rate (%)",
                value=self.category.taxes if self.category else 0.0,
                min=0,
                max=100,
            ).props("outlined")
            self.taxes_input.classes("w-full")

            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Cancel").on_click(self._on_cancel).props("outlined")
                ui.button(self.button_label, color="primary").on_click(self._on_submit)

    def _on_submit(self) -> None:
        """Handle form submission."""
        name = self.name_input.value
        taxes = self.taxes_input.value

        if not name or not name.strip():
            ui.notify("Please enter a category name", type="negative")
            return

        if taxes < 0 or taxes > 100:
            ui.notify("Tax rate must be between 0 and 100", type="negative")
            return

        self.on_submit(name, taxes)

    def _on_cancel(self) -> None:
        """Handle cancel - navigate back."""
        ui.navigate.back()

    def get_values(self) -> tuple[str, float]:
        """Get form values."""
        return self.name_input.value, self.taxes_input.value


class CategoryCard:
    """Reusable category card component for display."""

    def __init__(
        self,
        category: CategorySchema,
        on_edit: Optional[Callable[[int], None]] = None,
        on_delete: Optional[Callable[[int], None]] = None,
    ):
        """
        Initialize category card.
        
        Args:
            category: Category to display
            on_edit: Callback when edit button is clicked
            on_delete: Callback when delete button is clicked
        """
        self.category = category
        self.on_edit = on_edit
        self.on_delete = on_delete

    def render(self) -> None:
        """Render the category card."""
        with ui.card().classes("w-full"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column():
                    ui.label(self.category.name).classes("text-base font-bold")
                    ui.label(f"Tax Rate: {self.category.taxes}%").classes("text-sm text-gray-600")
                    ui.label(f"Products: {self.category.product_count}").classes("text-sm text-gray-600")

                with ui.row():
                    if self.on_edit:
                        ui.button(
                            "Edit",
                            icon="edit",
                            color="primary",
                        ).on_click(lambda: self.on_edit(self.category.category_id)).props("flat")

                    if self.on_delete:
                        ui.button(
                            "Delete",
                            icon="delete",
                            color="negative",
                        ).on_click(lambda: self.on_delete(self.category.category_id)).props("flat")
