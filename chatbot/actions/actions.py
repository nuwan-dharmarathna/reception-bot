from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.db_connect import db_connection


class ActionFetchMenu(Action):
    def name(self) -> Text:
        return "action_fetch_menu"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            conn, cursor = db_connection()
            
            if conn and cursor:
                cursor.execute("SELECT item_name, price FROM menu WHERE availability = TRUE")
                menu = cursor.fetchall()
                menu_text = ""
                for item in menu:
                    menu_text += f"{item[0]} - {item[1]}\n"
            
                dispatcher.utter_message(text=f"Our menu:\n{menu_text}")
            else:
                dispatcher.utter_message(text="Sorry, could not fetch the menu. Please try again later.")
        except Exception as e:
            dispatcher.utter_message(text="Sorry, could not fetch the menu DB issue. Please try again later.")
            print(e)
        finally:
            cursor.close()
            conn.close()
            
        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
