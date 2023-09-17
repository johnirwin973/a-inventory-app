from ._anvil_designer import Data_uploadTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Data_upload(Data_uploadTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    has_privileges = anvil.server.call_s('check_privileges')
    if not has_privileges:
        self.full_inventory.visible = False
        
    else:
        self.full_inventory.visible = True
        
    self.drop_down.items = ["Books", "Booklets", "Pamphlets", "Key Tags", "Chips", "Medallions",
                                "Service Items", "Specialty Items", "Multimedia Products",
                                "Tri Plate Laser", "Etched Medallions"]
    

  def full_inventory_change(self, file, **event_args):
    anvil.server.call_s('import_csv', file)
    open_form('Home')
    
  def update_prices_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    anvil.server.call_s('update_prices_quantity', file)
    open_form('Home')
    
  def add_to_inventory_button_click(self, **event_args):
        # Get input values from the input boxes and file upload
        self.label_error.visible = False
        error = self.sync_data()
        if error:
          self.label_error.text = error
          self.label_error.visible = True
          return
        category = self.drop_down.selected_value
        description = self.description_box.text
        item_number = self.item_number.text
        cost = self.cost_box.text
        cost_without_dollar = cost.lstrip('$') if cost else ''
        image = self.image_upload.file

        # Insert a new row into the "Inventory" table
        anvil.server.call_s('add_inventory_item', category, description, item_number, cost, image)
        anvil.alert("Upload is complete. Item added to inventory.")
        self.clear_info()
    
  def image_upload_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.image_1.source = file

  def drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def sync_data(self):
    if not self.drop_down.selected_value:
      return "Category is Required"
      
    if not self.description_box.text:
      return "Name is Required"
       
    if not self.item_number.text:
      return "Item number is Required"

    if not self.cost_box.text:
      return "Cost is Required"
      
    return None

  def clear_info(self):
    self.drop_down.selected_value = None
    self.description_box.text = ''
    self.item_number.text = ''
    self.cost_box.text = ''
    self.image_1.source = None

  def image_update_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.image_2.source = file

  def image_update_error(self):
    if not self.image_number.text:
      return "Item number is Required"

    if not self.image_update.file:
            return "Please upload a new image."

  def update_image_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_error.visible = False
    error = self.image_update_error()
    if error:
      self.label_error_2.text = error
      self.label_error_2.visible = True
      return
    item_number = self.image_number.text
    new_image = self.image_update.file
    success = anvil.server.call_s('update_inventory_image', item_number, new_image)

    if success:
        anvil.alert("Image updated successfully.")
    else:
        anvil.alert("Item with the specified Item_number not found.")  

  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    item_number = self.Delete_item_box.text 
    result = anvil.server.call_s('delete_item_row', item_number)  

    if result:
        self.data_grid_1.items = []  
        anvil.alert("Row deleted successfully.")
          
  def find_button_click(self, **event_args):
     """This method is called when the button is clicked"""
     item_number = self.Delete_item_box.text
     items_found = anvil.server.call_s('search_inventory', item_number)
    
     self.repeating_panel_1.items = items_found
    
     if not items_found:

         anvil.alert("Item not found in the inventory.")
    
    



    

 

