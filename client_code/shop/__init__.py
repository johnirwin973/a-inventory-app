from ._anvil_designer import shopTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Inventory import Inventory


class shop(shopTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        products = anvil.server.call('get_inventory')
      
        for P in products:
            self.flexer_1.add_component(Inventory(item=P))

    def Search_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      search_query = self.search_box.text.lower()  # Retrieve the value from the text box and convert to lowercase
      products = anvil.server.call('get_inventory') 

      filtered_products = []
      for p in products:
          if search_query.lower() in p['Description'].lower() or search_query.lower() in p['Item_number'].lower() or search_query.lower() in p['Category'].lower():
          
            filtered_products.append(p)

      self.flexer_1.clear()  
      for p in filtered_products:
           self.flexer_1.add_component(Inventory(item=p))

    def show_more_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass



