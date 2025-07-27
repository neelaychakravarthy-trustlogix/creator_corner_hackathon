#!/usr/bin/env python3
"""
ZeroEntropy Similarity Search
Find the most similar top 10 examples using ZeroEntropy's agentic retrieval
"""

import os
import time
from typing import List, Dict, Any
from zeroentropy import ZeroEntropy

# Import secrets
try:
    from secrets import ZEROENTROPY_API_KEY, OPENAI_API_KEY, ENVIRONMENT
except ImportError:
    print("❌ Please create a secrets.py file with your API keys")
    exit(1)

class SimilaritySearchAgent:
    """ZeroEntropy Agent for similarity search and example retrieval"""
    
    def __init__(self, api_key: str = None):
        """Initialize ZeroEntropy client"""
        self.api_key = api_key or ZEROENTROPY_API_KEY
        if not self.api_key or self.api_key == "your_zeroentropy_api_key_here":
            raise ValueError("Please set your ZEROENTROPY_API_KEY in secrets.py")
        
        self.client = ZeroEntropy(api_key=self.api_key)
        self.collection_name = "hackathon_docs"
        
    def search_similar_examples(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for the most similar examples"""
        try:
            print(f"🔍 Searching for examples similar to: '{query}'")
            
            # Perform similarity search
            results = self.client.queries.top_documents(
                collection_name=self.collection_name,
                query=query,
                k=top_k,
                include_metadata=True
            )
            
            # Extract results
            documents = results.results
            
            print(f"✅ Found {len(documents)} similar examples")
            return documents
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    def display_similar_examples(self, query: str, top_k: int = 10):
        """Display the most similar examples in a formatted way"""
        results = self.search_similar_examples(query, top_k)
        
        if not results:
            print("❌ No similar examples found")
            return
        
        print(f"\n📊 Top {len(results)} Most Similar Examples for: '{query}'")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i:2d}. Similarity Score: {result.score:.3f}")
            print(f"    📄 Document: {result.path}")
            print(f"    📋 Metadata:")
            for key, value in result.metadata.items():
                print(f"       • {key}: {value}")
            print(f"    🔗 File URL: {result.file_url[:60]}...")
            print("-" * 60)
    
    def batch_similarity_search(self, queries: List[str], top_k: int = 10):
        """Perform similarity search on multiple queries"""
        print("🚀 Batch Similarity Search")
        print("=" * 50)
        
        for i, query in enumerate(queries, 1):
            print(f"\n{i}. Query: '{query}'")
            self.display_similar_examples(query, top_k)
            time.sleep(1)  # Small delay between searches
    
    def find_most_similar_by_category(self, category: str, top_k: int = 10):
        """Find the most similar examples within a specific category"""
        query = f"examples in category: {category}"
        print(f"🎯 Finding most similar examples in category: '{category}'")
        self.display_similar_examples(query, top_k)
    
    def semantic_similarity_search(self, text: str, top_k: int = 10):
        """Perform semantic similarity search"""
        print(f"🧠 Semantic Similarity Search for: '{text}'")
        self.display_similar_examples(text, top_k)

def main():
    """Main function to demonstrate similarity search capabilities"""
    print("🚀 ZeroEntropy Similarity Search Example")
    print("=" * 60)
    print(f"Environment: {ENVIRONMENT}")
    
    # Initialize agent
    try:
        agent = SimilaritySearchAgent()
        print("✅ ZeroEntropy similarity search agent initialized")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Example 1: Basic similarity search
    print("\n" + "="*60)
    print("📝 Example 1: Basic Similarity Search")
    print("="*60)
    
    basic_queries = [
        "machine learning algorithms",
        "document processing techniques",
        "AI applications in business"
    ]
    
    for query in basic_queries:
        agent.display_similar_examples(query, top_k=5)
        print("\n" + "-"*40)
    
    # Example 2: Category-based similarity search
    print("\n" + "="*60)
    print("📝 Example 2: Category-Based Similarity Search")
    print("="*60)
    
    categories = ["technology", "documentation", "tutorial"]
    for category in categories:
        agent.find_most_similar_by_category(category, top_k=3)
        print("\n" + "-"*40)
    
    # Example 3: Semantic similarity search
    print("\n" + "="*60)
    print("📝 Example 3: Semantic Similarity Search")
    print("="*60)
    
    semantic_queries = [
        "How to implement intelligent systems?",
        "Best practices for data organization",
        "Advanced search and retrieval methods"
    ]
    
    for query in semantic_queries:
        agent.semantic_similarity_search(query, top_k=3)
        print("\n" + "-"*40)
    
    # Example 4: Batch similarity search
    print("\n" + "="*60)
    print("📝 Example 4: Batch Similarity Search")
    print("="*60)
    
    batch_queries = [
        "artificial intelligence",
        "document indexing",
        "search algorithms",
        "machine learning"
    ]
    
    agent.batch_similarity_search(batch_queries, top_k=3)
    
    print("\n🎉 Similarity search examples completed successfully!")
    print("\n💡 Tips for using similarity search:")
    print("1. Use specific keywords for better results")
    print("2. Try different query formulations")
    print("3. Use category-based searches for focused results")
    print("4. Experiment with semantic queries for broader matches")

if __name__ == "__main__":
    main() 