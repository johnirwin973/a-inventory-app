import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
import tempfile
from anvil.pdf import PDFRenderer
from datetime import datetime, timedelta

current_time = datetime.utcnow()
gmt_minus4_time = current_time - timedelta(hours=4)
formatted_date = gmt_minus4_time.strftime("%b %d %Y")
date = formatted_date

@anvil.server.callable
def create_order_pdf():
    user = anvil.users.get_user()
    if user is None:
        return

    home_group = user['homegroup']
    media_object = PDFRenderer(filename=f'{home_group} Order.pdf {date}').render_form('Order_pdf')
    new_order = app_tables.database.add_row(HomeGroup_orders=media_object)
    return new_order  
  
@anvil.server.callable
def create_reorder_pdf():
    media_object = PDFRenderer(filename=f'Georgian Heartland Literature order {date}').render_form('Reorder_pdf')
    new_reorder = app_tables.database.add_row(Area_orders=media_object)
    return new_reorder  
  
@anvil.server.callable
def inventory_pdf():
    print("Generating PDF...")
    media_object = PDFRenderer(filename=f'GHASC Inventory list {date}').render_form('Inventory_pdf')
    print("PDF generated successfully.")
    return media_object
  
@anvil.server.callable
def send_pdf_email():
    user = anvil.users.get_user()
    if user is None:
        return 
    
    user_email = user['email'] 
    home_group = user['homegroup']
    anvil.email.send(
        from_name="GHASC LITERATURE",
        to=[user_email, "irwin36@gmail.com"],
        subject="GHASC ORDER",
        text="Thank you for your order.",
        attachments=PDFRenderer(filename=f'{home_group} Order {date}').render_form('Order_pdf')
    )
    return
  
  
@anvil.server.callable
def send_reorder_email(): 
    anvil.email.send(
        from_name="GHASC LITERATURE",
        to=["irwin36@gmail.com"],
        subject="Georgian Heartland Literature order",
        text="Thank you for your service.",
        attachments=PDFRenderer(filename=f'Georgian Heartland Literature order {date}').render_form('Reorder_pdf')
    )
    return

@anvil.server.callable
def update_order_total():
    rows = app_tables.orders.search()
    total = 0.0
    
    for row in rows:
        if row['subtotal'] is not None:
            try:
                total += float(row['subtotal'].replace('$', ''))
            except ValueError:
                pass
    
    total_formatted = f"${total:.2f}" 
    return total_formatted

@anvil.server.callable
def delete_table_rows(Orders):
  table = app_tables.orders
  table.delete_all_rows()

@anvil.server.callable
def calculate_quantity_difference():
    all_items = app_tables.inventory.search()

    for item in all_items:
        quantity = item['Quantity']
        stock_limit = item['stock_limit']

        if quantity is not None and stock_limit is not None and quantity > 0:
            difference = stock_limit - quantity
            item['quantity_difference'] = difference

            # Check if the item exists in the inventory data table
            reorder_item = app_tables.inventory.get(Item_number=item['Item_number'])
            if reorder_item:
                reorder_item['quantity_difference'] = difference
                reorder_item.update()
            else:
                app_tables.inventory.add_row(item)

            
            cost = item.get('Cost', '').replace('$', '')
            quantity_difference = item.get('quantity_difference')

            if quantity_difference is not None and cost != '':
                subtotal = float(cost) * quantity_difference
                item['subtotal'] = "${:.2f}".format(subtotal)
            else:
                item['subtotal'] = ''


