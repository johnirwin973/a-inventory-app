from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.users
import anvil.server
from ..shop import shop
from ..Cart import Cart
from ..Admin_Page import Admin_Page

class Home(HomeTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
    def admin_link_click(self, **event_args):
      """This method is called when the link is clicked"""
      if anvil.users.get_user():
          self.open_admin()  # Open Shop form in content panel
          self.label_1.text = 'Admin'  # Update label text with form name
      else:
          alert('You must be logged as admin in to access admin.')
      
    def logout_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        anvil.server.call('delete_table_rows', 'Orders')
        anvil.users.logout()
        open_form('LogIn')
        pass
    
    def shop_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        if anvil.users.get_user():
            self.open_shop()  # Open Shop form in content panel
            self.label_1.text = 'Shop'  # Update label text with form name
        else:
            alert('You must be logged in to access the shop.')
          
    def cart_link_click(self, **event_args):
      """This method is called when the link is clicked"""
      if anvil.users.get_user():
            self.open_cart()  # Open Shop form in content panel
            self.label_1.text = 'Shopping Cart'  # Update label text with form name
      else:
            alert('You must be logged in to access the shopping Cart.')

    def open_shop(self, **event_args):
        """Open Shop form in content panel"""
        self.content_panel.clear()
        shop_form = shop()
        self.content_panel.add_component(shop_form)

    def open_cart(self, **event_args):
      """This method is called when the link is clicked"""
      self.content_panel.clear()
      cart_form = Cart()
      self.content_panel.add_component(cart_form)

    def open_admin(self, **event_args):
      """This method is called when the link is clicked"""
      self.content_panel.clear()
      admin_form = Admin_Page()
      self.content_panel.add_component(admin_form)

    def admin_link_show(self, **event_args):
      """This method is called when the Link is shown on the screen"""
      is_admin = anvil.server.call('check_admin')
      if not is_admin:
          self.admin_link.visible = False  # Hide the object when not admin



    

 



















   
    







    


    


   

      


    



    
      

    


    










 

 
  

 
  

