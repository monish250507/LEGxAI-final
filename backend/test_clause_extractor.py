#!/usr/bin/env python3
"""
Test script for the clause extractor implementation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_extraction():
    """Test basic clause extraction functionality."""
    try:
        from clause_extractor import extract_clauses
        
        # Test with numbered clauses
        test_text = """
        1. The parties shall maintain confidentiality of all information shared.
        2. This agreement shall be governed by the laws of California.
        3. Either party may terminate this contract with 30 days written notice.
        
        Additional terms:
        a) The client must pay all fees within 15 days.
        b) The service provider will deliver all work on time.
        """
        
        clauses = extract_clauses(test_text)
        
        print(f"✓ Extracted {len(clauses)} clauses")
        
        # Check clause structure
        for clause in clauses:
            if 'clause_id' not in clause:
                print(f"✗ Missing clause_id in: {clause}")
                return False
            if 'text' not in clause:
                print(f"✗ Missing text in: {clause}")
                return False
            if not clause['text'].strip():
                print(f"✗ Empty text in clause: {clause}")
                return False
        
        print("✓ All clauses have correct structure")
        return True
        
    except Exception as e:
        print(f"✗ Basic extraction test failed: {e}")
        return False

def test_numbered_patterns():
    """Test extraction of numbered clauses."""
    try:
        from clause_extractor import extract_clauses
        
        test_text = """
        1. The Company shall provide services as specified.
        2. The Client shall pay the agreed fees.
        (3) Both parties must comply with applicable laws.
        4. This contract is effective immediately.
        """
        
        clauses = extract_clauses(test_text)
        
        if len(clauses) >= 3:
            print(f"✓ Numbered pattern extraction works: {len(clauses)} clauses found")
            return True
        else:
            print(f"✗ Numbered pattern extraction failed: only {len(clauses)} clauses found")
            return False
            
    except Exception as e:
        print(f"✗ Numbered pattern test failed: {e}")
        return False

def test_paragraph_extraction():
    """Test extraction of paragraph-based clauses."""
    try:
        from clause_extractor import extract_clauses
        
        test_text = """
        The parties agree to maintain confidentiality throughout the duration of this agreement.
        
        All disputes shall be resolved through arbitration in accordance with established rules.
        
        This contract may be amended only with written consent from both parties.
        """
        
        clauses = extract_clauses(test_text)
        
        if len(clauses) >= 2:
            print(f"✓ Paragraph extraction works: {len(clauses)} clauses found")
            return True
        else:
            print(f"✗ Paragraph extraction failed: only {len(clauses)} clauses found")
            return False
            
    except Exception as e:
        print(f"✗ Paragraph extraction test failed: {e}")
        return False

def test_empty_input():
    """Test handling of empty input."""
    try:
        from clause_extractor import extract_clauses
        
        # Test empty string
        clauses = extract_clauses("")
        if len(clauses) == 0:
            print("✓ Empty string handled correctly")
        else:
            print(f"✗ Empty string should return empty list, got: {len(clauses)}")
            return False
        
        # Test whitespace only
        clauses = extract_clauses("   \n\n   ")
        if len(clauses) == 0:
            print("✓ Whitespace-only string handled correctly")
        else:
            print(f"✗ Whitespace-only string should return empty list, got: {len(clauses)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Empty input test failed: {e}")
        return False

def test_clause_ids():
    """Test that clause IDs are generated correctly."""
    try:
        from clause_extractor import extract_clauses
        
        test_text = """
        1. First clause with important information.
        2. Second clause with additional terms.
        3. Third clause with final conditions.
        """
        
        clauses = extract_clauses(test_text)
        
        # Check clause IDs format
        expected_ids = [f"clause_{i:03d}" for i in range(1, len(clauses) + 1)]
        actual_ids = [clause['clause_id'] for clause in clauses]
        
        if actual_ids == expected_ids:
            print("✓ Clause IDs generated correctly")
            return True
        else:
            print(f"✗ Clause IDs incorrect. Expected: {expected_ids}, Got: {actual_ids}")
            return False
            
    except Exception as e:
        print(f"✗ Clause ID test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Clause Extractor Test Suite")
    print("=" * 40)
    
    tests = [
        test_basic_extraction,
        test_numbered_patterns,
        test_paragraph_extraction,
        test_empty_input,
        test_clause_ids
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
        print("✓ All tests passed! Clause extractor is working correctly.")
        print("\nExample usage:")
        print("  from clause_extractor import extract_clauses")
        print("  clauses = extract_clauses(document_text)")
        print("  for clause in clauses:")
        print("      print(f\"{clause['clause_id']}: {clause['text']}\")")
        return 0
    else:
        print("⚠ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
