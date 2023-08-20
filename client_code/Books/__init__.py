from ._anvil_designer import BooksTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Books(BooksTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
  
        self.repeating_panel_1.items = app_tables.inventory.search(Category=q.any_of('Books', 'Booklets'))

    def search_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.repeating_panel_1.items = anvil.server.call('search_books', self.search_box.text)

  

        