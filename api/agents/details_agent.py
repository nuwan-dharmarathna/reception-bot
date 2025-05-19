from openai import OpenAI
from dotenv import load_dotenv
from copy import deepcopy
from .utils import get_chatbot_response, get_embedding
from pinecone import Pinecone
import os
import json
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

class DetailsAgent(object):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model_name = os.getenv("MODEL_NAME")
        self.embedding_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.pinecone = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY"),
        )
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
    
    def get_closest_results(self, index_name, input_emmbeddings, top_k=2):
        index = self.pinecone.Index(index_name)
        
        results = index.query(
            namespace="ns1",
            vector=input_emmbeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True,
        )
        
        return results
    
    def get_response(self, messages):
        messages = deepcopy(messages)
        
        last_user_message = messages[-1]["content"]
        
        embeddings = get_embedding(
            embedding_client=self.embedding_client,
            model_name=os.getenv("OPENAI_EMBEDDING_MODEL_NAME"),
            text_input=last_user_message
        )[0]
        
        results = self.get_closest_results(
            index_name=self.index_name,
            input_emmbeddings=embeddings
        )
        
        source_knowladge = "\n".join([result["metadata"]["text"].strip()+ "\n" for result in results['matches']])
        
        prompt = f"""
            Using the contexts below, answer the query.

            Contexts:
            {source_knowladge}

            Query: {last_user_message}
        """
        
        system_prompt = """
            You are a customer support agent for a coffee shop called Merry's way. You should answer every question as if you are waiter and provide the neccessary information to the user regarding their orders
        """
        
        messages[-1]["content"] = prompt
        
        imput_messages = [{"role" : "system", "content": system_prompt}] + messages[-3:]
        
        chatbot_output = get_chatbot_response(
            client=self.client,
            model_name=self.model_name,
            messages=imput_messages
        )
        
        output = self.postprocess_response(chatbot_output)
        
        return output
    
    def postprocess_response(self, response):
        
        output = {
            "role": "assistant",
            "content": response,
            "memory": {"agent":"details_agent"}
        }
        
        return output