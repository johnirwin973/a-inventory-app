from ._anvil_designer import Books_RowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Books_Row(Books_RowTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.update_subtotal()
    # Any code you write here will run before the form opens.

  def update_subtotal(self):
    rows = app_tables.inventory.search()
    subtotal = 0.0
    item_number = self.item_number_label.text  

    for row in rows:
      if row['Item_number'] == item_number:
        cost = row['Cost'].replace('$', '')
        quantity_text = self.Quantity_box.text  
        if cost is not None and quantity_text and quantity_text and int(quantity_text) > 0:
          quantity = int(quantity_text)
          subtotal += float(cost) * quantity  
          row['Total'] = "${:.2f}".format(float(cost) * quantity)  
        else:
          row['Total'] = ''  
        row.update()  

    self.subtotal_label.text = "${:.2f}".format(subtotal)

  def update_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    item_number = self.item_number_label.text
    quantity_text = self.Quantity_box.text
    if quantity_text and quantity_text:  
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
        inventory_item['stock_limit'] = update_limit
        inventory_item.update()
    else:
        print("Item number not found in the inventory table.")