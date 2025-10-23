"""
RAG (Retrieval-Augmented Generation) service
"""
import logging
from typing import List, Dict, Any
from database import Database
from config import MAX_RETRIEVAL_RESULTS

logger = logging.getLogger(__name__)


class RAGService:
    """Class for managing RAG information retrieval"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def retrieve(self, query: str, max_results: int = MAX_RETRIEVAL_RESULTS) -> List[Dict[str, Any]]:
        """
        Retrieve products related to query from database
        
        Args:
            query: Search text
            max_results: Maximum number of results
        
        Returns:
            List of related products
        """
        try:
            # Search in database
            products = self.db.search_products(query, limit=max_results)
            
            logger.info(f"Found {len(products)} products for query '{query}'")
            
            return products
        
        except Exception as e:
            logger.error(f"Error retrieving products: {e}")
            return []
    
    def retrieve_with_scoring(self, query: str, max_results: int = MAX_RETRIEVAL_RESULTS) -> List[Dict[str, Any]]:
        """
        Retrieve products with scoring (advanced version)
        
        In this version, more complex algorithms like TF-IDF or 
        embedding-based search can be added
        """
        # Currently using simple retrieve
        return self.retrieve(query, max_results)

