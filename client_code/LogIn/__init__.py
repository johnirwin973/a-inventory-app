from ._anvil_designer import LogInTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LogIn(LogInTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
        user = anvil.users.login_with_form(allow_cancel=True)
        if user is not None:
            open_form('Home')
    except TypeError:
        # Handle the cancel scenario here
        print("Login cancelled")
