import sys
import os
sys.path.append('ai')

from dotenv import load_dotenv
load_dotenv()

from performance_optimizer import get_performance_optimizer
from generative_service import GenerativeService

print("🔍 Testing Performance Optimization:")

# Test performance optimizer
print("\n1. Testing performance optimizer...")
optimizer = get_performance_optimizer()

# Test caching
test_text = "All citizens shall have the right to freedom of speech and expression"
print(f"   Cache hits: {optimizer.cache_hits}")
print(f"   Cache misses: {optimizer.cache_misses}")

# Test embedding caching
cached_embedding = optimizer.get_cached_embedding(test_text)
print(f"   Cached embedding found: {'✅' if cached_embedding else '❌'}")

# Cache an embedding
test_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
optimizer.cache_embedding(test_text, test_embedding)
print("   ✅ Embedding cached")

# Test retrieval
cached_embedding = optimizer.get_cached_embedding(test_text)
print(f"   Cached embedding found after caching: {'✅' if cached_embedding else '❌'}")

# Test API caching
print("\n2. Testing API caching...")
service = GenerativeService()

# Test first call (should hit API)
print("   First API call (should hit API)...")
result1 = service.generate_full_clause_analysis(
    test_text, 
    "US Constitution", 
    "fundamental_rights"
)
print(f"   Result 1 explanation length: {len(result1.get('explanation', ''))}")

# Test second call (should hit cache)
print("   Second API call (should hit cache)...")
result2 = service.generate_full_clause_analysis(
    test_text, 
    "US Constitution", 
    "fundamental_rights"
)
print(f"   Result 2 explanation length: {len(result2.get('explanation', ''))}")

# Test performance stats
print("\n3. Performance statistics:")
stats = optimizer.get_performance_stats()
print(f"   Cache hits: {stats['cache_hits']}")
print(f"   Cache misses: {stats['cache_misses']}")
print(f"   Hit rate: {stats['hit_rate_percent']}%")
print(f"   API calls: {stats['api_calls']}")
print(f"   Embedding cache size: {stats['embedding_cache_size']}")
print(f"   API cache size: {stats['api_cache_size']}")

print("\n📋 Performance optimization testing completed.")
