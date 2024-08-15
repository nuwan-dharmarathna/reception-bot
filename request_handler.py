from fastapi.responses import JSONResponse
from datetime import datetime

import db_handle

inprogress_orders ={}

def show_menu(parameters:dict, session_id:str, fullfilment_text:str):
    print("Showing menu")
    
    # Get the current time
    current_hour = datetime.now().hour
    
    # Determine the meal time based on the current hour
    if 6 <= current_hour < 11:
        meal_time = 'breakfast'
    elif 11 <= current_hour < 15:
        meal_time = 'lunch'
    else:
        meal_time = 'dinner'
        
    # Get the menu from DB
    menu = db_handle.show_menu(meal_time)
    
    fullfilment = fullfilment_text + f"\n\n{menu}"
    return JSONResponse(content={"fulfillmentText": fullfilment})

def order_add(parameters:dict, session_id:str, fullfilment_text:str):
    pass

def order_remove(parameters:dict, session_id:str, fullfilment_text:str):
    pass

def order_complete(parameters:dict, session_id:str, fullfilment_text:str):
    pass

def track_order(parameters:dict, session_id:str, fullfilment_text:str):
    pass