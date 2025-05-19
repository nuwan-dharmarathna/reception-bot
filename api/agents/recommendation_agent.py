from openai import OpenAI
from dotenv import load_dotenv
from copy import deepcopy
from .utils import get_chatbot_response
from pinecone import Pinecone
import pandas as pd
import os
import json
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)


class RecommendationAgent(object):
    def __init__(self, apriori_path, popular_recommendation_path):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model_name = os.getenv("MODEL_NAME")
        self.embedding_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        with open(apriori_path, 'r') as f:
            self.apriori_recommendations = json.load(f)

        self.popular_recommendations = pd.read_csv(popular_recommendation_path)
        self.products = self.popular_recommendations['product'].tolist()
        self.product_categories = self.popular_recommendations['product_category'].tolist()
        
    def apriori_recommendation(self, products, top_k=5):
        recommendation_list = []
        
        for product in products:
            if product in self.apriori_recommendations:
                recommendation_list += self.apriori_recommendations[product]
                
        # sort the recommendations by their confidence
        recommendation_list = sorted(recommendation_list, key=lambda x: x["confidence"], reverse=True)
        
        recommendations = []
        recommendations_per_category = {}
        
        for recommendation in recommendation_list:
            if recommendation in recommendations:
                continue
            
            # Limit 2 recommendations per category
            product_category = recommendation["product_category"]
            
            if product_category not in recommendations_per_category:
                recommendations_per_category[product_category] = 0
                
            if recommendations_per_category[product_category] >= 2:
                continue
            
            recommendations_per_category[product_category] += 1
            
            # Add recommendation to the list
            recommendations.append(recommendation["product"])
            
            if len(recommendations) >= top_k:
                break
            
        return recommendations
                
    
    def get_popular_recommendation(self,product_categories=None,top_k=5):
        recommendations_df = self.popular_recommendations
        
        if type(product_categories) == str:
            product_categories = [product_categories]

        if product_categories is not None:
            recommendations_df = self.popular_recommendations[self.popular_recommendations['product_category'].isin(product_categories)]
        recommendations_df = recommendations_df.sort_values(by='count',ascending=False)
        
        if recommendations_df.shape[0] == 0:
            return []

        recommendations = recommendations_df['product'].tolist()[:top_k]
        return recommendations
