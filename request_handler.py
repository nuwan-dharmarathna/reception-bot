from fastapi.responses import JSONResponse

import db_handle
import utils

inprogress_orders ={}


def show_menu(parameters:dict, session_id:str, fullfilment_text:str):
    
    #get the current time
    time = utils.get_current_time()
    
    # Get the menu from DB
    menu = db_handle.show_menu(time)
    
    fullfilment = fullfilment_text + f"\n\n{menu}"
    return JSONResponse(content={"fulfillmentText": fullfilment})

def order_add(parameters:dict, session_id:str, fullfilment_text:str):
    item_name = parameters['food_item']
    quantity = parameters['number']
    
    #get current time
    time = utils.get_current_time()
    
    # qty as int
    quantity_as_int = [int(q) for q in quantity]
    
    if len(item_name) != len(quantity):
        return JSONResponse(
            content={
                "fulfillmentText": "Please specify food items and their quantity correctly"
            }
        )
    else:
        order_dict = dict(zip(item_name, quantity_as_int))
        
        #check items in the menu
        res = db_handle.check_order_item(item_name, time)
        checked_items = [item[0] for item in res]
        
        # Filtered Dict
        filtered_order_dict = {key: value for key, value in order_dict.items() if key in checked_items}
        
        if session_id in inprogress_orders:
            current_order = inprogress_orders[session_id]
            current_order.update(filtered_order_dict)
            
            inprogress_orders[session_id] = current_order
        else:
            inprogress_orders[session_id] = filtered_order_dict
        
        fulfillment = f"{utils.format_order(inprogress_orders[session_id])}.\n " + fullfilment_text
        
        return JSONResponse(
            content={
                "fulfillmentText": fulfillment
            }
        )
    
def order_remove(parameters:dict, session_id:str, fullfilment_text:str):
    pass

def order_complete(parameters:dict, session_id:str, fullfilment_text:str):
    pass

def track_order(parameters:dict, session_id:str, fullfilment_text:str):
    order_id = int(parameters['number'])
    print(f"order_id: {order_id}")
    
    fullfilment = f"Your order id hit the backend #{order_id}"
    
    return JSONResponse(content={"fulfillmentText": fullfilment})
    