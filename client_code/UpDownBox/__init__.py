from ._anvil_designer import UpDownBoxTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class UpDownBox(UpDownBoxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def up_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    current_value = int(self.Quantity_box.text)
    self.Quantity_box.text = str(current_value + 1)

  def down_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    current_value = int(self.Quantity_box.text)
    if current_value > 0:
       self.Quantity_box.text = str(current_value - 1)


