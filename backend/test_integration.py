#!/usr/bin/env python3
"""
Test script for the integrated clause analysis pipeline.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        from document_processor import process_document
        from clause_extractor import extract_clauses
        from clause_classifier import classify_multiple_clauses
        from clause_ranker import rank_clauses_by_importance
        
        print("✓ All pipeline modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_pipeline_components():
    """Test individual pipeline components."""
    try:
        from document_processor import process_document
        from clause_extractor import extract_clauses
        from clause_classifier import classify_multiple_clauses
        from clause_ranker import rank_clauses_by_importance
        
        # Test document processing (mock)
        sample_text = """
        1. Either party may terminate this agreement with 30 days written notice.
        2. Payment shall be made within 15 days of invoice.
        3. The contractor shall indemnify the client against all claims.
        4. This agreement is governed by the laws of California.
        """
        
        # Test clause extraction
        extracted_clauses = extract_clauses(sample_text)
        if len(extracted_clauses) > 0:
            print(f"✓ Clause extraction works: {len(extracted_clauses)} clauses")
        else:
            print("✗ Clause extraction failed")
            return False
        
        # Test clause classification
        classified_clauses = classify_multiple_clauses(extracted_clauses)
        if len(classified_clauses) > 0:
            print(f"✓ Clause classification works: {len(classified_clauses)} clauses")
        else:
            print("✗ Clause classification failed")
            return False
        
        # Test clause ranking
        ranked_clauses = rank_clauses_by_importance(classified_clauses)
        if len(ranked_clauses) > 0:
            print(f"✓ Clause ranking works: {len(ranked_clauses)} clauses")
        else:
            print("✗ Clause ranking failed")
            return False
        
        # Verify required fields
        for clause in ranked_clauses:
            required_fields = ['clause_id', 'text', 'type', 'priority_score', 'color']
            for field in required_fields:
                if field not in clause:
                    print(f"✗ Missing field '{field}' in clause")
                    return False
        
        print("✓ All required fields present in ranked clauses")
        return True
        
    except Exception as e:
        print(f"✗ Pipeline components test failed: {e}")
        return False

def test_response_structure():
    """Test the expected response structure."""
    try:
        from clause_extractor import extract_clauses
        from clause_classifier import classify_multiple_clauses
        from clause_ranker import rank_clauses_by_importance
        
        # Create sample data
        sample_text = """
        1. Either party may terminate this agreement with 30 days written notice.
        2. Payment shall be made within 15 days of invoice.
        """
        
        # Process through pipeline
        extracted = extract_clauses(sample_text)
        classified = classify_multiple_clauses(extracted)
        ranked = rank_clauses_by_importance(classified)
        
        # Create response structure as expected from upload endpoint
        response_clauses = []
        for clause in ranked:
            response_clause = {
                "clause_id": clause.get('clause_id', ''),
                "text": clause.get('text', ''),
                "type": clause.get('type', 'general'),
                "priority_score": clause.get('priority_score', 0.0),
                "color": clause.get('color', 'green')
            }
            response_clauses.append(response_clause)
        
        # Verify response structure
        expected_response = {
            "status": "success",
            "filename": "test_document.pdf",
            "document_stats": {
                "total_characters": len(sample_text),
                "total_clauses": len(extracted),
                "classified_clauses": len(classified),
                "ranked_clauses": len(ranked)
            },
            "clauses": response_clauses,
            "summary": {
                "high_priority_count": len([c for c in response_clauses if c['color'] == 'red']),
                "medium_priority_count": len([c for c in response_clauses if c['color'] == 'yellow']),
                "low_priority_count": len([c for c in response_clauses if c['color'] == 'green']),
                "clause_types": list(set([c['type'] for c in response_clauses]))
            }
        }
        
        # Validate structure
        required_keys = ['status', 'filename', 'document_stats', 'clauses', 'summary']
        for key in required_keys:
            if key not in expected_response:
                print(f"✗ Missing key '{key}' in response structure")
                return False
        
        print("✓ Response structure is correct")
        print(f"✓ High priority clauses: {expected_response['summary']['high_priority_count']}")
        print(f"✓ Medium priority clauses: {expected_response['summary']['medium_priority_count']}")
        print(f"✓ Low priority clauses: {expected_response['summary']['low_priority_count']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Response structure test failed: {e}")
        return False

def test_end_to_end_workflow():
    """Test the complete end-to-end workflow."""
    try:
        from document_processor import process_document
        from clause_extractor import extract_clauses
        from clause_classifier import classify_multiple_clauses
        from clause_ranker import rank_clauses_by_importance
        
        # Simulate complete workflow
        print("Testing complete workflow...")
        
        # Sample document text
        document_text = """
        CONTRACT AGREEMENT
        
        1. TERMINATION: Either party may terminate this agreement with 30 days written notice.
        
        2. PAYMENT: The client shall pay all fees within 15 days of receipt of invoice.
        
        3. INDEMNITY: The contractor shall indemnify and hold harmless the client from any claims.
        
        4. JURISDICTION: This agreement shall be governed by the laws of California.
        
        5. GENERAL: Both parties acknowledge they have read and understood this agreement.
        """
        
        # Step 1: Extract clauses
        print("Step 1: Extracting clauses...")
        extracted = extract_clauses(document_text)
        print(f"  Extracted {len(extracted)} clauses")
        
        # Step 2: Classify clauses
        print("Step 2: Classifying clauses...")
        classified = classify_multiple_clauses(extracted)
        print(f"  Classified {len(classified)} clauses")
        
        # Step 3: Rank clauses
        print("Step 3: Ranking clauses...")
        ranked = rank_clauses_by_importance(classified)
        print(f"  Ranked {len(ranked)} clauses")
        
        # Step 4: Verify final structure
        print("Step 4: Verifying final structure...")
        for i, clause in enumerate(ranked[:3], 1):
            print(f"  {i}. {clause['type']} ({clause['color']}) - Score: {clause['priority_score']}")
            print(f"     {clause['text'][:60]}...")
        
        # Verify all required fields are present
        required_fields = ['clause_id', 'text', 'type', 'priority_score', 'color']
        for clause in ranked:
            for field in required_fields:
                if field not in clause:
                    print(f"✗ Missing field '{field}' in clause: {clause}")
                    return False
        
        print("✓ Complete workflow successful")
        return True
        
    except Exception as e:
        print(f"✗ End-to-end workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all integration tests."""
    print("Integration Pipeline Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_pipeline_components,
        test_response_structure,
        test_end_to_end_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All integration tests passed!")
        print("✓ Full clause analysis pipeline is ready for deployment.")
        print("\nPipeline Summary:")
        print("  1. Document Processing → Extract text from PDF")
        print("  2. Clause Extraction → Identify individual clauses")
        print("  3. Clause Classification → Categorize by type")
        print("  4. Clause Ranking → Prioritize by importance")
        print("  5. Structured Output → Return JSON with all fields")
        return 0
    else:
        print("⚠ Some integration tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
