"""
Database initialization and verification script
"""
from database import Database
from config import DB_PATH
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Initialize and verify database"""
    logger.info("=== Database Initialization ===")
    
    # Create database
    db = Database()
    logger.info(f"Database created at {DB_PATH}")
    
    # Check product count
    products = db.get_all_products()
    logger.info(f"Total products: {len(products)}")
    
    # Show sample products
    logger.info("\n=== Sample Products ===")
    for i, product in enumerate(products[:5], 1):
        logger.info(f"{i}. {product['name']} - Price: {product['price']:,.0f} تومان")
    
    # Test search
    logger.info("\n=== Search Test ===")
    test_queries = ["گوشی", "لپ‌تاپ", "آیفون", "سامسونگ"]
    
    for query in test_queries:
        results = db.search_products(query, limit=3)
        logger.info(f"\nSearch: '{query}' - {len(results)} results found")
        for product in results:
            logger.info(f"  - {product['name']}")
    
    logger.info("\n✅ Database initialized successfully!")


if __name__ == "__main__":
    main()

