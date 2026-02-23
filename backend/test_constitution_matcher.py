import sys
import os
sys.path.append('ai')

from constitution_matcher import ConstitutionMatcher
from embedding_service import load_model

print("🔍 Testing Constitution Matcher:")

# Load embedding model
load_model()

# Initialize constitution matcher
matcher = ConstitutionMatcher()

# Test loading constitutions
print("\n1. Loading constitutions...")
success = matcher.load_constitutions()
print(f"   Loading: {'✅' if success else '❌'}")

# Test constitution matching
print("\n2. Testing constitution matching...")
test_clause = "All citizens shall have the right to freedom of speech and expression"

# Test with COI constitution
matches = matcher.match_constitution_sections(test_clause, "COI", top_k=3)
print(f"   COI matches: {len(matches)}")
for i, match in enumerate(matches[:2]):
    print(f"     {i+1}. Article {match['article_number']} (Score: {match['similarity_score']:.3f})")
    print(f"        Title: {match['title'][:50]}...")

# Test best match
best_match = matcher.get_best_match(test_clause, "COI")
if best_match:
    print(f"   Best match: Article {best_match['article_number']} (Score: {best_match['similarity_score']:.3f})")

# Test search all constitutions
print("\n3. Testing search across all constitutions...")
all_matches = matcher.search_all_constitutions(test_clause, top_k=1)
print(f"   Constitutions with matches: {len(all_matches)}")
for const_name, matches in all_matches.items():
    print(f"   {const_name}: {len(matches)} matches")

print("\n📋 Constitution matcher testing completed.")
