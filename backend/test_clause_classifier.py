#!/usr/bin/env python3
"""
Test script for the clause classifier implementation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_keyword_classification():
    """Test keyword-based classification functionality."""
    try:
        # Import the classifier functions directly
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_classifier", "clause_classifier.py")
        clause_classifier = importlib.util.module_from_spec(spec)
        
        # Mock the AI pipeline import
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"type": "general", "confidence": 0.5}'
        sys.modules['services.ai_pipeline'] = ai_pipeline
        
        spec.loader.exec_module(clause_classifier)
        
        # Test termination clause
        termination_text = "Either party may terminate this agreement with 30 days written notice."
        result = clause_classifier.classify_clause_type(termination_text)
        
        if result['type'] == 'termination':
            print("✓ Termination clause classified correctly")
        else:
            print(f"✗ Termination clause misclassified as: {result['type']}")
            return False
        
        # Test payment clause
        payment_text = "The client shall pay all fees within 15 days of invoice."
        result = clause_classifier.classify_clause_type(payment_text)
        
        if result['type'] == 'payment':
            print("✓ Payment clause classified correctly")
        else:
            print(f"✗ Payment clause misclassified as: {result['type']}")
            return False
        
        # Test confidentiality clause
        confidentiality_text = "Both parties shall maintain confidentiality of all proprietary information."
        result = clause_classifier.classify_clause_type(confidentiality_text)
        
        if result['type'] == 'confidentiality':
            print("✓ Confidentiality clause classified correctly")
        else:
            print(f"✗ Confidentiality clause misclassified as: {result['type']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Keyword classification test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_clauses():
    """Test classification of multiple clauses."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_classifier", "clause_classifier.py")
        clause_classifier = importlib.util.module_from_spec(spec)
        
        # Mock AI pipeline
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"type": "general", "confidence": 0.5}'
        sys.modules['services.ai_pipeline'] = ai_pipeline
        
        spec.loader.exec_module(clause_classifier)
        
        test_clauses = [
            "The parties shall maintain confidentiality of all information shared.",
            "Payment shall be made within 30 days of receipt of invoice.",
            "This agreement is governed by the laws of California.",
            "Either party may terminate this contract with written notice.",
            "The service provider shall be liable for any damages caused."
        ]
        
        results = clause_classifier.classify_multiple_clauses(test_clauses)
        
        if len(results) == len(test_clauses):
            print(f"✓ Multiple clause classification works: {len(results)} clauses processed")
        else:
            print(f"✗ Multiple clause classification failed: expected {len(test_clauses)}, got {len(results)}")
            return False
        
        # Check that all results have required fields
        for result in results:
            if 'type' not in result:
                print(f"✗ Missing type field in result: {result}")
                return False
            if 'confidence' not in result:
                print(f"✗ Missing confidence field in result: {result}")
                return False
        
        print("✓ All results have correct structure")
        return True
        
    except Exception as e:
        print(f"✗ Multiple clauses test failed: {e}")
        return False

def test_confidence_scores():
    """Test that confidence scores are reasonable."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_classifier", "clause_classifier.py")
        clause_classifier = importlib.util.module_from_spec(spec)
        
        # Mock AI pipeline
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"type": "general", "confidence": 0.5}'
        sys.modules['services.ai_pipeline'] = ai_pipeline
        
        spec.loader.exec_module(clause_classifier)
        
        # Test with strong keyword match
        strong_text = "TERMINATE TERMINATION TERMINATE"
        result = clause_classifier.classify_clause_type(strong_text)
        
        if 0.0 <= result['confidence'] <= 1.0:
            print(f"✓ Confidence score in valid range: {result['confidence']}")
        else:
            print(f"✗ Invalid confidence score: {result['confidence']}")
            return False
        
        # Test with weak keyword match
        weak_text = "The parties agree to general terms."
        result = clause_classifier.classify_clause_type(weak_text)
        
        if 0.0 <= result['confidence'] <= 1.0:
            print(f"✓ Weak match confidence score valid: {result['confidence']}")
        else:
            print(f"✗ Invalid weak match confidence: {result['confidence']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Confidence score test failed: {e}")
        return False

def test_all_clause_types():
    """Test that all required clause types can be detected."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_classifier", "clause_classifier.py")
        clause_classifier = importlib.util.module_from_spec(spec)
        
        # Mock AI pipeline
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"type": "general", "confidence": 0.5}'
        sys.modules['services.ai_pipeline'] = ai_pipeline
        
        spec.loader.exec_module(clause_classifier)
        
        test_cases = [
            ("termination", "Either party may terminate this agreement."),
            ("liability", "The service provider shall be liable for damages."),
            ("payment", "Payment shall be made within 30 days."),
            ("jurisdiction", "This agreement is governed by California law."),
            ("confidentiality", "All information shall be kept confidential."),
            ("indemnity", "The contractor shall indemnify the client."),
            ("general", "The parties acknowledge the terms herein.")
        ]
        
        detected_types = set()
        for expected_type, test_text in test_cases:
            result = clause_classifier.classify_clause_type(test_text)
            detected_type = result['type']
            detected_types.add(detected_type)
            
            if detected_type == expected_type:
                print(f"✓ {expected_type} clause detected correctly")
            else:
                print(f"⚠ {expected_type} clause detected as {detected_type}")
        
        # Check if all types are detectable
        required_types = {'termination', 'liability', 'payment', 'jurisdiction', 
                         'confidentiality', 'indemnity', 'general'}
        
        if required_types.issubset(detected_types):
            print("✓ All required clause types are detectable")
            return True
        else:
            missing = required_types - detected_types
            print(f"✗ Missing clause types: {missing}")
            return False
        
    except Exception as e:
        print(f"✗ All clause types test failed: {e}")
        return False

def test_statistics_function():
    """Test the statistics function."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("clause_classifier", "clause_classifier.py")
        clause_classifier = importlib.util.module_from_spec(spec)
        
        # Mock AI pipeline
        import types
        ai_pipeline = types.ModuleType('ai_pipeline')
        ai_pipeline._call_chat = lambda *args, **kwargs: '{"type": "general", "confidence": 0.5}'
        sys.modules['services.ai_pipeline'] = ai_pipeline
        
        spec.loader.exec_module(clause_classifier)
        
        test_clauses = [
            {"text": "Payment clause", "type": "payment", "confidence": 0.8},
            {"text": "Termination clause", "type": "termination", "confidence": 0.9},
            {"text": "General clause", "type": "general", "confidence": 0.6}
        ]
        
        stats = clause_classifier.get_clause_type_statistics(test_clauses)
        
        if 'total_clauses' in stats and stats['total_clauses'] == 3:
            print("✓ Statistics function works correctly")
        else:
            print(f"✗ Statistics function failed: {stats}")
            return False
        
        if 'type_distribution' in stats:
            print("✓ Type distribution calculated")
        else:
            print("✗ Type distribution missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Statistics function test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Clause Classifier Test Suite")
    print("=" * 40)
    
    tests = [
        test_keyword_classification,
        test_multiple_clauses,
        test_confidence_scores,
        test_all_clause_types,
        test_statistics_function
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
        print("✓ All tests passed! Clause classifier is working correctly.")
        print("\nExample usage:")
        print("  from clause_classifier import classify_clause_type")
        print("  result = classify_clause_type('Payment shall be made within 30 days.')")
        print("  print(f\"Type: {result['type']}, Confidence: {result['confidence']}\")")
        return 0
    else:
        print("⚠ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
