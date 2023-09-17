from ._anvil_designer import KeyTagsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class KeyTags(KeyTagsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = app_tables.inventory.search(Category=q.any_of('KeyTags', 'Chips', 'Bronze Medallions'))
 
  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.items = anvil.server.call_s('search_keys', self.search_box.text)

  
