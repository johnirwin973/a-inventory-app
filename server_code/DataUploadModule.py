import anvil.email
import anvil.media
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import openpyxl


@anvil.server.callable
def import_csv(file):
    with anvil.media.TempFile(file) as temp_file:
        with open(temp_file, "r", encoding='latin-1') as f:
            csv_data = f.readlines()
            rows = [row.strip().split(",") for row in csv_data]
            column_headers = rows[0]
            item_number_column = "Item_number"  
            cost_column = "Cost" 
            image_column = "Image"  
            for row in rows[1:]:
                row_data = dict(zip(column_headers, row))
                item_number = row_data[item_number_column]
                existing_row = app_tables.inventory.get(Item_number=item_number)
                if existing_row is not None:
                   
                    if existing_row[cost_column] != row_data[cost_column]:
                        existing_row[cost_column] = row_data[cost_column]
                    
                    if image_column in existing_row:
                        row_data[image_column] = existing_row[image_column]
                    existing_row.update()
                else:
                    
                    app_tables.inventory.add_row(**row_data)


@anvil.server.callable
def update_prices(file):
    with anvil.media.TempFile(file) as temp_file:
        with open(temp_file, "r", encoding='latin-1') as f:
            csv_data = f.readlines()
            rows = [row.strip().split(",") for row in csv_data]
            column_headers = rows[0]
            item_number_column = "Item_number"  
            cost_column = "Cost"  
            data_dict = {row_data[column_headers.index(item_number_column)]: row_data[column_headers.index(cost_column)] for row_data in rows[1:]}  
            inventory_table = app_tables.inventory.search()
            for row in inventory_table:
                item_number = row[item_number_column]
                if item_number in data_dict:
                    row[cost_column] = data_dict[item_number]
                    row.update()  


@anvil.server.callable
def add_inventory_item(category, description, item_number, cost, image):
    app_tables.inventory.add_row(Category=category, Description=description, Item_number=item_number, Cost=cost, Images=image)

@anvil.server.callable
def update_inventory_image(item_number, new_image):
    item = app_tables.inventory.get(Item_number=item_number)
    if item:
        item['Images'] = new_image
        item.update()
        return True
    else:
        return False

@anvil.server.callable
def delete_item_row(item_number):
    # Search for the row with the given item_number
    rows = app_tables.inventory.search(Item_number=item_number)
    
    # Check if the row exists
    if len(rows) > 0:
        # Get the first row (assuming there's only one row with the given item_number)
        row = rows[0]
        # Delete the row from the data table
        row.delete()
    else:
        # Row with the given item_number not found
        raise Exception("Item not found in the inventory.")
  