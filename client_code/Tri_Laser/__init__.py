from ._anvil_designer import Tri_LaserTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Tri_Laser(Tri_LaserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    self.repeating_panel_1.items = self.fetch_tri_data()
    
  
  def fetch_tri_data(self):
    category_1_results = list(app_tables.inventory.search(Category='TRIPLATE MEDALLIONS'))
    category_2_results = list(app_tables.inventory.search(Category='LASER-ETCHED MEDALLIONS'))

    combined_results = category_1_results + category_2_results

    return combined_results

  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.items = anvil.server.call_s('search_Tri_items', self.search_box.text)


