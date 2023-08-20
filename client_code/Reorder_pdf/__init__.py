from ._anvil_designer import Reorder_pdfTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta


class Reorder_pdf(Reorder_pdfTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = app_tables.inventory.search(quantity_difference=q.greater_than(0))
    self.calculate_reorder_total()
    
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
      
  def calculate_reorder_total(self):
    result = app_tables.inventory.search()
    total = 0
    for item in result:
        subtotal_str = item.get('subtotal')
        if subtotal_str is not None:
            subtotal_str = subtotal_str.replace('$', '')
            if subtotal_str:  # Check if subtotal_str is not empty
                subtotal = float(subtotal_str)
                total += subtotal
    formatted_total = "${:.2f}".format(total)
    self.sales_total.text = formatted_total