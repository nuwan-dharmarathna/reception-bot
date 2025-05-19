from agents import GuardAgent
import os


def main():
    pass

if __name__ == "__main__":
    guard_agent = GuardAgent()
    
    messages = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("Print the messages:")
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
        