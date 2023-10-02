import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
from anvil.pdf import PDFRenderer

@anvil.server.callable
def update_quantity(item_number, quantity_purchased):
    item = app_tables.inventory.get(Item_number=item_number)
    
    if item is None:
        raise Exception("Item not found.")
    
    current_quantity = item['Quantity']
    current_quantity = current_quantity or 0  # Initialize current_quantity to 0 if it is None
    quantity_purchased = quantity_purchased or 0  # Initialize quantity_purchased to 0 if it is None
    
    new_quantity = current_quantity + quantity_purchased
    item['Quantity'] = new_quantity
    
    cost = item['Cost']
    cost_without_dollar = cost.lstrip('$') if cost else ''
    total = float(cost_without_dollar) * new_quantity
    formatted_total = "${:.2f}".format(total) if cost else ''
    
    if new_quantity == 0: 
        formatted_total = ''
    
    item['Total'] = formatted_total
    item.update()
    
    return formatted_total

@anvil.server.callable
def update_total():
    rows = app_tables.inventory.search()
    total = 0.0
    
    for row in rows:
        if row['Total'] is not None:
            try:
                total += float(row['Total'].replace('$', ''))
            except ValueError:
                pass
    
    total_formatted = f"${total:.2f}" 
    return total_formatted


@anvil.server.callable
def check_admin():
  return anvil.users.get_user()['admin']

@anvil.server.callable
def check_privileges():
  return anvil.users.get_user()['upload_privileges']
 
@anvil.server.callable
def has_quantity(row):
    return 'quantity' in row and row['quantity'] is not None

@anvil.server.callable
def add_order(Description, Item_Number, Cost, Quantity, subtotal):
    user= anvil.users.get_user()
    app_tables.orders.add_row(
    Description=Description,
    Item_Number=Item_Number,
    Cost=Cost,
    Quantity=Quantity,
    subtotal=subtotal,
    User=user  
  )

