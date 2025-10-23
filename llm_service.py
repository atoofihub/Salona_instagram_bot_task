"""
LLM service for connecting to Gemini API
"""
import os
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)


class LLMService:
    """Class for managing connection to Google Gemini API"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        if not api_key:
            raise ValueError(
                "Gemini API key not set. "
                "Please set the GEMINI_API_KEY environment variable."
            )
        
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
    
    def generate_response(
        self,
        user_message: str,
        retrieved_products: List[Dict[str, Any]]
    ) -> str:
        """Generate intelligent response based on user message and retrieved products"""
        try:
            prompt = self._build_prompt(user_message, retrieved_products)
            response = self.model.generate_content(prompt)
            
            if not response.text:
                logger.warning("Empty response received from Gemini")
                return self._fallback_response(retrieved_products)
            
            return response.text.strip()
        
        except Exception as e:
            logger.error(f"Error generating response from Gemini: {e}")
            return self._fallback_response(retrieved_products)
    
    def _build_prompt(
        self,
        user_message: str,
        retrieved_products: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for sending to LLM"""
        
        if not retrieved_products:
            prompt = f"""You are an online store assistant that responds in Persian.
The user sent a message but no related products were found in the database.

User message: {user_message}

Please inform the user in Persian and in a friendly tone that unfortunately we couldn't find the product they're looking for and ask them to ask their question more clearly or mention another product name.
"""
            return prompt
        
        products_text = ""
        for i, product in enumerate(retrieved_products, 1):
            price_formatted = f"{product['price']:,.0f}".replace(',', '،')
            products_text += f"""
Product {i}:
Name: {product['name']}
Description: {product['description']}
Price: {price_formatted} تومان
---
"""
        
        prompt = f"""You are an online store assistant that responds in Persian.
Your task is to help customers find and buy products.

User message: {user_message}

Related products found:
{products_text}

Instructions:
1. Write the response completely in Persian
2. If the user asks about price, mention prices clearly and with Persian numbers
3. If the user asks about specifications, give complete descriptions
4. If multiple similar products are found, introduce all of them and mention their differences
5. Use a friendly and professional tone
6. Keep the response short and useful (maximum 3-4 sentences)
7. If possible, provide a smart recommendation based on user needs
8. Don't use English numbers, all numbers should be Persian
9. Use Persian numbers instead of English ones

Response:"""
        
        return prompt
    
    def _fallback_response(self, retrieved_products: List[Dict[str, Any]]) -> str:
        """Fallback response in case of LLM error"""
        if not retrieved_products:
            return "متاسفانه محصول مورد نظر شما را پیدا نکردم. لطفا سوال خود را واضح‌تر مطرح کنید."
        
        if len(retrieved_products) == 1:
            product = retrieved_products[0]
            price_formatted = f"{product['price']:,.0f}".replace(',', '،')
            return f"{product['name']} با قیمت {price_formatted} تومان موجود است."
        else:
            response = f"تعداد {len(retrieved_products)} محصول مرتبط پیدا شد:\n"
            for product in retrieved_products[:3]:
                price_formatted = f"{product['price']:,.0f}".replace(',', '،')
                response += f"- {product['name']}: {price_formatted} تومان\n"
            return response

