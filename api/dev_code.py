from agents import (GuardAgent, ClassificationAgent, DetailsAgent, AgentProtocol, RecommendationAgent)
import os
from typing import Dict
import pathlib

folder_path = pathlib.Path(__file__).parent.resolve()


def main():
    pass

if __name__ == "__main__":
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    
    agent_dict: dict[str, AgentProtocol] = {
        "details_agent" : DetailsAgent(),
        "recommendation_agent" : RecommendationAgent(
            apriori_path=os.path.join(folder_path, "recommendation_objects/apriori_recommendations.json"),
            popular_recommendation_path=os.path.join(folder_path, "recommendation_objects/popularity_recommendation.csv")
        )
    }
    
    messages = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("Print the messages........")
        for message in messages:
            print(f"{message['role']} : {message['content']}")
            
        # Get user input
        prompt = input("Enter your message: ")
        messages.append({"role": "user", "content": prompt})
        
        # get Guard agent response
        response = guard_agent.get_response(messages)
        if response["memory"]["guard_decision"] == "not allowed":
            messages.append(response)
            continue
    
        #  Get Classification Agent's response
        classification_response = classification_agent.get_response(messages)
        
        chosen_agent = classification_response["memory"]["classification_decision"]
        print(f"Chosen agent: {chosen_agent}")
        
        # Get the chosen agent's response
        agent = agent_dict[chosen_agent]
        agent_response = agent.get_response(messages)
        
        messages.append(agent_response)
