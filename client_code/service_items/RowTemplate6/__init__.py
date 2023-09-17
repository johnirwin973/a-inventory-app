from ._anvil_designer import RowTemplate6Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate6(RowTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.update_subtotal()
    # Any code you write here will run before the form opens.

  def update_subtotal(self):
    rows = app_tables.inventory.search()
    subtotal = 0.0
    item_number = self.item_number_label.text  # Assuming you have a label component to display the item number

    for row in rows:
      if row['Item_number'] == item_number:
        cost = row['Cost'].replace('$', '')
        quantity_text = self.Quantity_box.text  # Get the value from the Quantity_box text box
        if cost is not None and quantity_text and quantity_text and int(quantity_text) > 0:
          quantity = int(quantity_text)
          subtotal += float(cost) * quantity  # Accumulate the subtotal for each item
          row['Total'] = "${:.2f}".format(float(cost) * quantity)  # Update the 'Total' column
        else:
          row['Total'] = ''  # Clear the 'Total' column if quantity is empty, blank, or zero
        row.update()  # Update the row in the inventory table

    self.subtotal_label.text = "${:.2f}".format(subtotal)

  def update_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    item_number = self.item_number_label.text
    quantity_text = self.Quantity_box.text
    if quantity_text and quantity_text:  # Check if the text is not None and not blank after removing leading/trailing whitespace
        quantity_purchased = int(quantity_text)
    else:
        quantity_purchased = None

    
    self.update_subtotal()
    self.update_stock_limit()

  def update_stock_limit(self):
    update_limit = self.stock_limit_box.text
    item_number = self.item_number_label.text

  
    inventory_item = app_tables.inventory.get(Item_number=item_number)

    if inventory_item:
        # Update the stock_limit column of the found inventory item
        inventory_item['stock_limit'] = update_limit
        inventory_item.update()
    else:
        # Handle the case when the item number is not found in the inventory table
        print("Item number not found in the inventory table.")


  

