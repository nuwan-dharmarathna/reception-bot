from datetime import datetime
import re

def extract_session_id(session_str: str):
    matcher = re.search(r"/sessions/(.*?)/contexts", session_str)
    if matcher:
        session_id = matcher.group(1)
        return session_id
    return None

def format_order(order: dict):
    formatted_order = ', '.join(f'{key} - {value}' for key, value in order.items())
    
    return formatted_order

def get_current_time():
    # Get the current time
    current_hour = datetime.now().hour
    
    # Determine the meal time based on the current hour
    if 6 <= current_hour < 11:
        meal_time = 'breakfast'
    elif 11 <= current_hour < 15:
        meal_time = 'lunch'
    else:
        meal_time = 'dinner'
    
    return meal_time