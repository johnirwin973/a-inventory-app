from ._anvil_designer import Order_pdfTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class Order_pdf(Order_pdfTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    current_time = datetime.utcnow()
    gmt_minus4_time = current_time - timedelta(hours=4)
    formatted_date = gmt_minus4_time.strftime("%b %d %Y %H:%M")
    self.date_label.text = formatted_date

    user = anvil.users.get_user()
    self.name_box.text = user['name']
    self.city_box.text = user['city']
    self.homegroup_box.text = user['homegroup']
    self.email_box.text = user['email']
    self.phone_box.text = user['phone']
    self.repeating_panel_1.items = app_tables.orders.search()
    self.sales_total.text = anvil.server.call_s('update_order_total')
   
    