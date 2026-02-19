#!/usr/bin/env python3
"""
Test script for the clause ranker implementation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_priority_scores():
    """Test that priority scores are assigned correctly."""
    try:
        # Import the ranker functions directly
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_ranker", "clause_ranker.py")
        clause_ranker = importlib.util.module_from_spec(spec)
        
        # Mock the dependencies
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"importance_score": 5}'
        
        embeddings = types.ModuleType('embeddings')
        embeddings.encode_texts = lambda texts: [[0.1] * len(texts) for _ in texts]
        
        sys.modules['services.ai_pipeline'] = ai_pipeline
        sys.modules['services.embeddings'] = embeddings
        
        spec.loader.exec_module(clause_ranker)
        
        # Test priority score assignment
        test_clauses = [
            {"text": "Either party may terminate this agreement.", "type": "termination"},
            {"text": "The provider shall be liable for damages.", "type": "liability"},
            {"text": "The contractor shall indemnify the client.", "type": "indemnity"},
            {"text": "Payment shall be made within 30 days.", "type": "payment"},
            {"text": "General terms and conditions.", "type": "general"}
        ]
        
        results = clause_ranker.rank_clauses_by_importance(test_clauses)
        
        # Check priority scores
        expected_scores = {
            'termination': 0.9,
            'liability': 0.85,
            'indemnity': 0.8,
            'payment': 0.6,
            'general': 0.3
        }
        
        for result in results:
            clause_type = result.get('type', 'general')
            expected_score = expected_scores.get(clause_type, 0.3)
            actual_score = result.get('priority_score', 0)
            
            if abs(actual_score - expected_score) < 0.01:
                print(f"✓ {clause_type} priority score correct: {actual_score}")
            else:
                print(f"✗ {clause_type} priority score incorrect: expected {expected_score}, got {actual_score}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Priority scores test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_color_coding():
    """Test that color coding is applied correctly."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_ranker", "clause_ranker.py")
        clause_ranker = importlib.util.module_from_spec(spec)
        
        # Mock dependencies
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"importance_score": 5}'
        embeddings = types.ModuleType('embeddings')
        embeddings.encode_texts = lambda texts: [[0.1] * len(texts) for _ in texts]
        
        sys.modules['services.ai_pipeline'] = ai_pipeline
        sys.modules['services.embeddings'] = embeddings
        
        spec.loader.exec_module(clause_ranker)
        
        # Test color assignment
        test_cases = [
            (0.9, 'red'),    # High priority
            (0.8, 'red'),    # High priority
            (0.6, 'yellow'), # Medium priority
            (0.5, 'yellow'), # Medium priority
            (0.3, 'green'),  # Low priority
            (0.1, 'green')   # Low priority
        ]
        
        for score, expected_color in test_cases:
            actual_color = clause_ranker.get_priority_color(score)
            if actual_color == expected_color:
                print(f"✓ Score {score} → Color {actual_color}")
            else:
                print(f"✗ Score {score} color incorrect: expected {expected_color}, got {actual_color}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Color coding test failed: {e}")
        return False

def test_ranking_order():
    """Test that clauses are ranked in correct order."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_ranker", "clause_ranker.py")
        clause_ranker = importlib.util.module_from_spec(spec)
        
        # Mock dependencies
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"importance_score": 5}'
        embeddings = types.ModuleType('embeddings')
        embeddings.encode_texts = lambda texts: [[0.1] * len(texts) for _ in texts]
        
        sys.modules['services.ai_pipeline'] = ai_pipeline
        sys.modules['services.embeddings'] = embeddings
        
        spec.loader.exec_module(clause_ranker)
        
        # Test ranking order (should be highest priority first)
        test_clauses = [
            {"text": "General clause", "type": "general"},
            {"text": "Payment clause", "type": "payment"},
            {"text": "Termination clause", "type": "termination"},
            {"text": "Liability clause", "type": "liability"}
        ]
        
        results = clause_ranker.rank_clauses_by_importance(test_clauses)
        
        # Check that results are sorted by priority score (descending)
        scores = [result['priority_score'] for result in results]
        if scores == sorted(scores, reverse=True):
            print("✓ Clauses ranked correctly by priority")
        else:
            print(f"✗ Clauses not ranked correctly: {scores}")
            return False
        
        # Check that highest priority clause is first
        if results[0]['type'] == 'termination':
            print("✓ Highest priority clause ranked first")
        else:
            print(f"✗ Wrong clause ranked first: {results[0]['type']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Ranking order test failed: {e}")
        return False

def test_statistics_function():
    """Test the statistics function."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_ranker", "clause_ranker.py")
        clause_ranker = importlib.util.module_from_spec(spec)
        
        # Mock dependencies
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"importance_score": 5}'
        embeddings = types.ModuleType('embeddings')
        embeddings.encode_texts = lambda texts: [[0.1] * len(texts) for _ in texts]
        
        sys.modules['services.ai_pipeline'] = ai_pipeline
        sys.modules['services.embeddings'] = embeddings
        
        spec.loader.exec_module(clause_ranker)
        
        test_clauses = [
            {"text": "Termination clause", "type": "termination", "color": "red"},
            {"text": "Payment clause", "type": "payment", "color": "yellow"},
            {"text": "General clause", "type": "general", "color": "green"}
        ]
        
        stats = clause_ranker.get_clause_priority_statistics(test_clauses)
        
        if 'total_clauses' in stats and stats['total_clauses'] == 3:
            print("✓ Statistics function works correctly")
        else:
            print(f"✗ Statistics function failed: {stats}")
            return False
        
        if 'priority_distribution' in stats:
            dist = stats['priority_distribution']
            if dist['counts'].get('red', 0) == 1:
                print("✓ Red priority count correct")
            else:
                print(f"✗ Red priority count incorrect: {dist['counts']}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Statistics function test failed: {e}")
        return False

def test_complete_workflow():
    """Test the complete workflow with all fields."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_ranker", "clause_ranker.py")
        clause_ranker = importlib.util.module_from_spec(spec)
        
        # Mock dependencies
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"importance_score": 5}'
        embeddings = types.ModuleType('embeddings')
        embeddings.encode_texts = lambda texts: [[0.1] * len(texts) for _ in texts]
        
        sys.modules['services.ai_pipeline'] = ai_pipeline
        sys.modules['services.embeddings'] = embeddings
        
        spec.loader.exec_module(clause_ranker)
        
        test_clauses = [
            {"clause_id": "clause_001", "text": "Either party may terminate this agreement.", "type": "termination"},
            {"clause_id": "clause_002", "text": "Payment shall be made within 30 days.", "type": "payment"},
            {"clause_id": "clause_003", "text": "The contractor shall indemnify the client.", "type": "indemnity"}
        ]
        
        results = clause_ranker.rank_clauses_by_importance(test_clauses)
        
        # Check that all required fields are present
        required_fields = ['clause_id', 'text', 'type', 'priority_score', 'color', 'rank', 'combined_score']
        
        for result in results:
            for field in required_fields:
                if field not in result:
                    print(f"✗ Missing field '{field}' in result: {result}")
                    return False
        
        print("✓ All required fields present in results")
        
        # Check specific values
        termination_clause = next((r for r in results if r['type'] == 'termination'), None)
        if termination_clause and termination_clause['color'] == 'red':
            print("✓ Termination clause has correct color (red)")
        else:
            print(f"✗ Termination clause color incorrect: {termination_clause}")
            return False
        
        payment_clause = next((r for r in results if r['type'] == 'payment'), None)
        if payment_clause and payment_clause['color'] == 'yellow':
            print("✓ Payment clause has correct color (yellow)")
        else:
            print(f"✗ Payment clause color incorrect: {payment_clause}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Complete workflow test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Clause Ranker Test Suite")
    print("=" * 40)
    
    tests = [
        test_priority_scores,
        test_color_coding,
        test_ranking_order,
        test_statistics_function,
        test_complete_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Clause ranker is working correctly.")
        print("\nExample usage:")
        print("  from clause_ranker import rank_clauses_by_importance")
        print("  clauses = [{'text': 'Payment clause', 'type': 'payment'}]")
        print("  ranked = rank_clauses_by_importance(clauses)")
        print("  for clause in ranked:")
        print("      print(f\"{clause['type']}: {clause['priority_score']} ({clause['color']})\")")
        return 0
    else:
        print("⚠ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
