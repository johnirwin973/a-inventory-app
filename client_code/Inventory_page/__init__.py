from ._anvil_designer import Inventory_pageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Inventory_page(Inventory_pageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.sales_total.text = anvil.server.call_s('update_total')
        self.rp_reorder_list.items = app_tables.inventory.search(Quantity=q.greater_than(0))
        
    
    def download_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      pdf = anvil.server.call('inventory_pdf')
      download(pdf)
      open_form('Home')

 
        

 

    
