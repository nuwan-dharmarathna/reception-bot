from fastapi import FastAPI, Request

import utils
import request_handler

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    # Retrive the json data from the request
    
    data = await request.json()
    
    
    intent = data['queryResult']['intent']['displayName']
    parameters = data['queryResult']['parameters']
    outputContexts = data['queryResult']['outputContexts']
    try:
        fulfillment_text = data['queryResult']['fulfillmentText']
    except KeyError:
        fulfillment_text = ""
    
    # Extract the session id from the output contexts
    session_id = utils.extract_session_id(outputContexts[1]['name'])
    
    intent_handler = {
        "new_order-context:ongoing-order": request_handler.show_menu,
        "order_add-context:ongoing-order": request_handler.order_add,
        "order_remove-context:ongoing-order": request_handler.order_remove,
        "order_complete-context:ongoing-order": request_handler.order_complete,
        "track_order-context:ongoing_tracking": request_handler.track_order,
        "order_type-context:finalizing-order": request_handler.add_order_type,
    }
    
    return intent_handler[intent](parameters, session_id, fulfillment_text)


    