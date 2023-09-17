from ._anvil_designer import PamphletsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pamphlets(PamphletsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.repeating_panel_4.items = app_tables.inventory.search(Category=q.full_text_match('Pamphletes'))
  
  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.items = anvil.server.call_s('search_pamphlets', self.search_box.text)


