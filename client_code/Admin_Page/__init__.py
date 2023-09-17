from ._anvil_designer import Admin_PageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Books import Books
from ..Inventory_page import Inventory_page
from ..Pamphlets import Pamphlets
from ..KeyTags import KeyTags
from ..Multi_media import Multi_media
from ..service_items import service_items
from ..special_items import special_items
from ..Tri_Laser import Tri_Laser
from ..Data_upload import Data_upload
from ..Reorder_Form import Reorder_Form


class Admin_Page(Admin_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.server.call_s('calculate_quantity_difference')
    
    self.drop_down.items = ["Inventory List", "Place Regional order", "Books/Booklets", "Pamphlets", "Key Tags, Chips & Medallions",
                                "Service Items", "Specialty Items", "Multimedia Products",
                                "Tri Plate & Laser Etched Medallions", "Update inventory database"]
       
    self.drop_down.set_event_handler("change", self.drop_down_change)

  def drop_down_change(self, **event_args):
      """This method is called when an item is selected"""
      selected_item = self.drop_down.selected_value

      if selected_item == "Inventory List":
            self.open_inventory_page()
      elif selected_item == "Place Regional order":
            self.open_reorder_page()
      elif selected_item == "Books/Booklets":
            self.open_books_form()
      elif selected_item == "Pamphlets":
            self.open_pamphlets_form()
      elif selected_item == "Key Tags, Chips & Medallions":
            self.open_keytags_form()
      elif selected_item == "Service Items":
            self.open_service_items()
      elif selected_item == "Specialty Items":
            self.open_special_items()
      elif selected_item == "Multimedia Products":
            self.open_media()
      elif selected_item == "Tri Plate & Laser Etched Medallions":
            self.open_tri()
      elif selected_item == "Update inventory database":
            self.open_upload()
        
  def open_books_form(self, **event_args):
        """Open Books form in content panel"""
        self.content_panel.clear()
        books_form = Books()
        self.content_panel.add_component(books_form)
    
  def open_inventory_page(self, **event_args):
        """Open Inventory page in content panel"""
        self.content_panel.clear()
        inventory_page = Inventory_page()
        self.content_panel.add_component(inventory_page)

  def open_reorder_page(self, **event_args):
        """Open Inventory page in content panel"""
        self.content_panel.clear()
        reorder_page = Reorder_Form()
        self.content_panel.add_component(reorder_page)
  
    
  def open_pamphlets_form(self, **event_args):
        """Open Pamphlets form in content panel"""
        self.content_panel.clear()
        pamphlets_form = Pamphlets()
        self.content_panel.add_component(pamphlets_form)
      
  def open_keytags_form(self, **event_args):
        """Open KeyTags form in content panel"""
        self.content_panel.clear()
        keys_form = KeyTags()
        self.content_panel.add_component(keys_form)

  def open_service_items(self, **event_args):
        """Open Service Items form in content panel"""
        self.content_panel.clear()
        service_form = service_items()
        self.content_panel.add_component(service_form)

  def open_special_items(self, **event_args):
        """Open Specialty Items form in content panel"""
        self.content_panel.clear()
        special_form = special_items()
        self.content_panel.add_component(special_form)

  def open_media(self, **event_args):
        """Open Multimedia form in content panel"""
        self.content_panel.clear()
        media_form = Multi_media() 
        self.content_panel.add_component(media_form)

  def open_upload(self, **event_args):
        """Open Data Upload form in content panel"""
        self.content_panel.clear()
        upload_form = Data_upload()
        self.content_panel.add_component(upload_form)

  def open_tri(self, **event_args):
        """Open Tri Plate form in content panel"""
        self.content_panel.clear()
        tri_form = Tri_Laser()
        self.content_panel.add_component(tri_form)

  



  












