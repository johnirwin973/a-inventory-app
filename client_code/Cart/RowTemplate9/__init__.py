from ._anvil_designer import RowTemplate9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Cart
from ...Home import Home



class RowTemplate9(RowTemplate9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
   

  
  def update_button_click(self, **event_args):
    """This method is called when the update button is clicked"""
    Item_Number = self.item_number_label.text
    Quantity = self.Quantity_box.text

    if not Quantity:
        Notification("Please specify a quantity").show()
    else:
        quantity_text = self.Quantity_box.text

        if quantity_text is None or quantity_text == "":
            message = "Please specify a quantity."
            alert(message)
            return

        desired_quantity = int(quantity_text)
        order = app_tables.orders.get(Item_Number=Item_Number)

        if order is not None:
            inventory_item = app_tables.inventory.get(Item_number=Item_Number)

            if inventory_item is not None:
                available_quantity = inventory_item['Quantity']
                if desired_quantity <= available_quantity:
                    cost_without_symbol = order['Cost'].replace('$', '')  # Remove dollar sign
                    cost_without_symbol = cost_without_symbol.replace(',', '')  # Remove commas if present
                    subtotal = float(cost_without_symbol) * desired_quantity  # Calculate new subtotal
                    # Format the new subtotal with a dollar sign
                    formatted_subtotal = "${:.2f}".format(subtotal)

                    # Update the quantity and subtotal in the orders data table
                    order['Quantity'] = desired_quantity
                    order['subtotal'] = formatted_subtotal
                    order.update()

                    message = f"Quantity updated: {desired_quantity}. Subtotal updated to {formatted_subtotal}."
                    alert(message)
                    
                    # Refresh the page to reflect the updated data
                    open_form('Home')
                    
                else:
                    message = f"Insufficient quantity. Only {available_quantity} items available."
                    alert(message)
            else:
                message = "Item not found in the inventory table."
                alert(message)
        else:
            message = "Order not found in the orders data table."
            alert(message)
  
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item.delete()
    self.remove_from_parent()
    open_form('Home')
    







    
    