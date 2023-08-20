from ._anvil_designer import UsersPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home
from ..Cart import Cart

class UsersPage(UsersPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    user = anvil.users.get_user()
    if user is not None:
      self.name_box.text = user['name']
      self.city_box.text = user['city']
      self.homegroup_box.text = user['homegroup']
      self.email_box.text = user['email']
      self.phone_box.text = user['phone']

    # Any code you write here will run before the form opens.
  
  def update_user_info(self, **event_args):
     user = anvil.users.get_user()
     user.update( 
       name = self.name_box.text,
       city = self.city_box.text,
       homegroup = self.homegroup_box.text,
       email = self.email_box.text,
       phone = self.phone_box.text
    )

  def sub_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_error.visible = False
    error = self.sync_data()
    if error:
     self.label_error.text = error
     self.label_error.visible = True
     return
    self.update_user_info()  
    anvil.server.call('create_order_pdf')
    anvil.server.call('send_pdf_email')
    rows = app_tables.orders.search()  
    for row in rows:
            item_number = row['Item_Number']
            quantity = row['Quantity']
            cost = float(row['Cost'].replace('$', ''))

            inventory_item = app_tables.inventory.get(Item_number=item_number)

            if inventory_item is not None:
                available_quantity = inventory_item['Quantity']

                if quantity is not None and available_quantity is not None:
                   if quantity <= available_quantity:
                    # Update the inventory quantity
                      inventory_item['Quantity'] -= quantity

                    # Update the inventory total
                      inventory_total = float(inventory_item['Total'].replace('$', ''))
                      inventory_item['Total'] = f"${inventory_total - (quantity * cost):.2f}"

                      inventory_item.update()
                      anvil.server.call('delete_table_rows', 'Orders')
                   else:
                      message = f"Insufficient quantity for item {item_number}. Only {available_quantity} items available."
                      alert(message)
                      return
                else:
                    message = f"Quantity or available quantity is None for item {item_number}."
                    alert(message)
                    return
            else:
                message = f"Item {item_number} not found in the inventory table."
                alert(message)
                return
    open_form('Home')


  def sync_data(self):
    if not self.name_box.text:
      return "Name Required"
      
    if not self.homegroup_box.text:
      return "Home Group Required"
       
    if not self.city_box.text:
      return "City is Required"

    if not self.email_box.text:
      return "Email is Required"

    if not self.phone_box.text:
      return "Phone number is Required"
      
    return None

    try:
      self.name = int(self.text_box_name.text)
      self.home_group = int(self.text_box_home_group.text)
      self.city = int(self.text_box_city.text)
    except TypeError as te:
      return "Invalid format"
    except Exception as x:
      return "Unknown error {}".format(x)
    return None  

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')
 