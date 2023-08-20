from ._anvil_designer import Reorder_FormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta


class Reorder_Form(Reorder_FormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        anvil.server.call('calculate_quantity_difference')
        self.calculate_reorder_total()
        self.repeating_panel_1.items = app_tables.inventory.search(quantity_difference=q.greater_than(0))
        current_time = datetime.utcnow()
        gmt_minus4_time = current_time - timedelta(hours=4)
        formatted_date = gmt_minus4_time.strftime("%b %d %Y %H:%M")
        self.date_label.text = formatted_date

        admin = app_tables.admin.search()
        if admin:
            first_admin = admin[0]  # Access the first row in the 'admin' table
            self.name_box.text = first_admin['name']
            self.area_name.text = first_admin['area_name']
            self.shipping_address.text = first_admin['shipping_address']
            self.email_box.text = first_admin['email']
            self.phone_box.text = first_admin['phone']

        

    def update_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        admin_table = app_tables.admin
        admin_rows = admin_table.search()

        if admin_rows:
            # Assuming there is only one row in the admin table, you can update its values
            admin_row = admin_rows[0]

            admin_row['name'] = self.name_box.text
            admin_row['area_name'] = self.area_name.text
            admin_row['shipping_address'] = self.shipping_address.text
            admin_row['email'] = self.email_box.text
            admin_row['phone'] = self.phone_box.text

            admin_row.update()

    def calculate_reorder_total(self):
        result = app_tables.inventory.search()
        total = 0
        for item in result:
            subtotal_str = item.get('subtotal')  # Use item.get('subtotal') to handle None values
            if subtotal_str:  # Check if subtotal_str is not empty
                subtotal_str = subtotal_str.replace('$', '')  # Replace '$' symbol
                subtotal = float(subtotal_str)
                total += subtotal

        total = abs(total)

        formatted_total = "${:.2f}".format(total)
        self.sales_total.text = formatted_total

    def submit_reorder_click(self, **event_args):
      """This method is called when the button is clicked"""
      items = self.repeating_panel_1.items
      if any(item['item_name'] for item in items):
          anvil.server.call('send_reorder_email')
          anvil.server.call('create_reorder_pdf')
          open_form('Home')
      else:
          alert("Cannot submit reorder. No items in list.")
      

    def order_recieved_click(self, **event_args):
      """This method is called when the button is clicked"""
      inventory_table = app_tables.inventory.search()
      for row in inventory_table:
        # Get the quantity difference for the current row
          quantity_difference = row['quantity_difference']
        
        # Get the current quantity for the row
          current_quantity = row['Quantity']
        
        # Update the quantity by adding the quantity difference
          if quantity_difference is not None and current_quantity is not None:
             updated_quantity = current_quantity + quantity_difference
             row['Quantity'] = updated_quantity
            
    # Make sure to open the 'Home' form after iterating through all rows
      open_form('Home')

      


 
        