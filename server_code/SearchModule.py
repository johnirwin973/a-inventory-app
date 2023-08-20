import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_inventory():
    inventory = app_tables.inventory.search()
    return inventory

@anvil.server.callable
def search_inventory(query):
    result = app_tables.inventory.search()
    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
                or query.lower() in x['Category'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
                or query in x['Category']
            ]
    return result
  
@anvil.server.callable
def search_books(query):
    result = app_tables.inventory.search(
        Category=q.any_of('Books', 'Booklets')
    )

    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
            ]
    return result

@anvil.server.callable
def search_pamphlets(query):
    result = app_tables.inventory.search(Category='Pamphlets')
    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
            ]
    return result

@anvil.server.callable
def search_service_items(query):
    result = app_tables.inventory.search(Category='Service Items')
    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
            ]
    return result

@anvil.server.callable
def search_Specialty_items(query):
    result = app_tables.inventory.search(Category='Specialty Items')
    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
            ]
    return result

@anvil.server.callable
def search_media_pro(query):
    result = app_tables.inventory.search(Category='Multimedia Products')
    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
            ]
    return result

@anvil.server.callable
def search_keys(query):
    result = app_tables.inventory.search(
        Category=q.any_of('Key Tags', 'Chips', 'Bronze Medallions'))
    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
            ]
    return result

@anvil.server.callable
def search_Tri_items(query):
    result = app_tables.inventory.search(
        Category=q.any_of('LASER-ETCHED MEDALLIONS', 'TRIPLATE MEDALLIONS')
    )

    if query is not None:
        query_string = '%{}%'.format(query)
        
        if query.islower():
            result = [
                x for x in result
                if query.lower() in x['Description'].lower()
                or query.lower() in x['Item_number'].lower()
            ]
        else:
            result = [
                x for x in result
                if query in x['Description']
                or query in x['Item_number']
            ]
    return result

