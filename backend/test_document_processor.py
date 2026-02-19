#!/usr/bin/env python3
"""
Test script for the document processor implementation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_import():
    """Test if the document processor can be imported."""
    try:
        from document_processor import DocumentProcessor, process_document
        print("✓ DocumentProcessor imported successfully")
        print("✓ process_document function imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_processor_initialization():
    """Test DocumentProcessor initialization."""
    try:
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        print(f"✓ DocumentProcessor initialized successfully")
        print(f"✓ Supported formats: {processor.supported_formats}")
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False

def test_text_cleaning():
    """Test text cleaning functionality."""
    try:
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        
        # Test with dirty text
        dirty_text = "  This   is a   test\x0c  with  artifacts!  "
        clean_text = processor._clean_text(dirty_text)
        
        expected = "This is a test with artifacts!"
        if clean_text == expected:
            print("✓ Text cleaning works correctly")
            return True
        else:
            print(f"✗ Text cleaning failed. Expected: '{expected}', Got: '{clean_text}'")
            return False
    except Exception as e:
        print(f"✗ Text cleaning test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Document Processor Test Suite")
    print("=" * 40)
    
    tests = [
        test_import,
        test_processor_initialization,
        test_text_cleaning
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
        print("✓ All tests passed! Document processor is ready.")
        return 0
    else:
        print("⚠ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
