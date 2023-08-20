from ._anvil_designer import Inventory_pdfTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class Inventory_pdf(Inventory_pdfTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Calculate Ontario time
        current_time = datetime.utcnow()
        gmt_minus4_time = current_time - timedelta(hours=4)
        formatted_date = gmt_minus4_time.strftime("%b %d %Y %H:%M")
        self.date_label.text = formatted_date


        self.repeating_panel_1.items = app_tables.inventory.search(Quantity=q.greater_than(0))
        self.sales_total.text = anvil.server.call('update_total')