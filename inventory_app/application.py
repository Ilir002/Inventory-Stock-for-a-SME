from nicegui import ui
from inventory_app.data_access.db import Database


class Application:

    def run(self) -> None:
        # DB initialisieren und Seed-Daten laden
        Database.init()
        from inventory_app.data_access.seed import seed_if_empty
        seed_if_empty()

        # UI starten
        from inventory_app.ui import pages  # noqa
        ui.run(title="Stefanelli Inventory", port=8080, reload=False, show=False)