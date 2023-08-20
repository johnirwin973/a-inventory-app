from ._anvil_designer import CartTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Cart(CartTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
      
        self.refresh_cart_items()

    def refresh_cart_items(self):
        # Remove existing items from the repeating panel
        self.repeating_panel_1.items = []

        rows = app_tables.orders.search()
        self.repeating_panel_1.items = rows 

        # Calculate the subtotal
        subtotal = sum(float(row['Cost'].replace('$', '')) * int(row['Quantity'])
    for row in rows
    if row['Cost'] is not None and row['Quantity'] is not None
)
        # Format the subtotal as a currency string
        subtotal_formatted = f"${subtotal:.2f}"
        self.total_label.text = subtotal_formatted
        
    def continue_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      if len(self.repeating_panel_1.items) == 0:  # Check if there are items in the cart
         alert("Cart is empty. Please add items before continuing.")
      else:
          open_form('UsersPage')

    


    
        
     
 


