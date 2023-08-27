from ._anvil_designer import InventoryTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Inventory(InventoryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    item = self.item
      
    if 'Quantity' in item:
        quantity = item['Quantity']
        if quantity is not None and quantity > 0:
            self.label_error.text = f"{quantity} In stock"
        else:
            self.label_error.text = "Out of stock"
    else:
        self.label_error.text = "Out of stock"  

  def add_to_cart_click(self, **event_args):
    """This method is called when the button is clicked"""
    Description = self.description_label.text
    Item_Number = self.Item_number_label.text
    Cost = self.price_label.text
    Quantity = self.shop_quantity_box.text
    
    if not Quantity:
        Notification("Please specify a quantity").show()
    else:
        quantity_text = self.shop_quantity_box.text

        if quantity_text is None or quantity_text == "":
            message = "Please specify a quantity."
            alert(message)
            return

        desired_quantity = int(quantity_text)
        inventory = app_tables.inventory.search()

        if len(inventory) > 0:
            item_number = self.Item_number_label.text
            available_quantity = None
            for row in inventory:
                if row['Item_number'] == item_number:
                    available_quantity = row['Quantity']
                    break

            if available_quantity is not None:
                if desired_quantity <= available_quantity:
                    cost_without_symbol = Cost.replace('$', '')  # Remove dollar sign
                    cost_without_symbol = cost_without_symbol.replace(',', '')  # Remove commas if present
                    item_cost = float(cost_without_symbol)
                    subtotal = item_cost * desired_quantity
                    formatted_subtotal = f"${subtotal:.2f}"
                    orders = app_tables.orders.search(Item_Number=Item_Number)
                    if len(orders) > 0:
                        existing_order = orders[0]
                        existing_quantity = existing_order['Quantity']
                        existing_subtotal = existing_order['subtotal']
                        existing_subtotal = existing_subtotal.replace('$', '')  # Remove dollar sign
                        existing_subtotal = existing_subtotal.replace(',', '')  # Remove commas if present
                        existing_subtotal = float(existing_subtotal)
                        new_quantity = existing_quantity + desired_quantity
                        new_subtotal = existing_subtotal + subtotal
                        existing_order['Quantity'] = new_quantity
                        existing_order['subtotal'] = f"${new_subtotal:.2f}"
                        existing_order.update()
                    else:
                        anvil.server.call('add_order', Description, Item_Number, Cost, Quantity, formatted_subtotal)  # Pass subtotal as an argument
                    self.shop_quantity_box.text = ""
                else:
                    message = f"Insufficient quantity. Only {available_quantity} items available."
                    alert(message)
            else:
                message = "None on hand, Please make another selection."
                alert(message)
        else:
            message = "Inventory not found."
            alert(message) 
    