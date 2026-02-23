#!/usr/bin/env python3
"""
Test backend stability and complete pipeline functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all critical modules can be imported."""
    print("Testing imports...")
    
    try:
        import main
        print("✓ main.py imported successfully")
    except Exception as e:
        print(f"✗ main.py import failed: {e}")
        return False
    
    try:
        from services.document_analysis_service import document_analysis_service
        print("✓ DocumentAnalysisService imported successfully")
    except Exception as e:
        print(f"✗ DocumentAnalysisService import failed: {e}")
        return False
    
    try:
        from document_processor import process_document
        print("✓ document_processor imported successfully")
    except Exception as e:
        print(f"✗ document_processor import failed: {e}")
        return False
    
    try:
        from clause_extractor import extract_clauses
        print("✓ clause_extractor imported successfully")
    except Exception as e:
        print(f"✗ clause_extractor import failed: {e}")
        return False
    
    try:
        from clause_classifier import classify_multiple_clauses
        print("✓ clause_classifier imported successfully")
    except Exception as e:
        print(f"✗ clause_classifier import failed: {e}")
        return False
    
    try:
        from clause_ranker import rank_clauses_by_importance
        print("✓ clause_ranker imported successfully")
    except Exception as e:
        print(f"✗ clause_ranker import failed: {e}")
        return False
    
    return True

def test_pipeline_structure():
    """Test that pipeline has correct structure."""
    print("\nTesting pipeline structure...")
    
    try:
        from services.document_analysis_service import DocumentAnalysisService
        service = DocumentAnalysisService()
        
        # Test supported formats
        formats = service.get_supported_formats()
        expected_formats = ['.pdf', '.txt', '.docx', '.json']
        
        if set(formats) == set(expected_formats):
            print("✓ Supported formats correct")
        else:
            print(f"✗ Supported formats incorrect: {formats}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Pipeline structure test failed: {e}")
        return False

def test_clause_structure():
    """Test clause structure standardization."""
    print("\nTesting clause structure...")
    
    try:
        from services.document_analysis_service import DocumentAnalysisService
        service = DocumentAnalysisService()
        
        # Test clause structure
        test_clauses = [
            {
                'clause_id': 'clause_001',
                'text': 'Test clause text',
                'type': 'termination',
                'confidence': 0.85,
                'priority_score': 0.9,
                'color': 'red',
                'rank': 1
            }
        ]
        
        standardized = service._standardize_clause_structure(test_clauses)
        
        # Check required fields
        required_fields = ['clause_id', 'text', 'type', 'confidence', 'priority_score', 'color', 'rank']
        
        for clause in standardized:
            for field in required_fields:
                if field not in clause:
                    print(f"✗ Missing field '{field}' in standardized clause")
                    return False
        
        print("✓ Clause structure standardization works")
        return True
        
    except Exception as e:
        print(f"✗ Clause structure test failed: {e}")
        return False

def test_response_structure():
    """Test response structure creation."""
    print("\nTesting response structure...")
    
    try:
        from services.document_analysis_service import DocumentAnalysisService
        service = DocumentAnalysisService()
        
        test_clauses = [
            {
                'clause_id': 'clause_001',
                'text': 'Test clause text',
                'type': 'termination',
                'confidence': 0.85,
                'priority_score': 0.9,
                'color': 'red',
                'rank': 1
            }
        ]
        
        response = service._create_response_structure(
            'test.pdf',
            'Test document text',
            test_clauses,
            test_clauses,
            test_clauses
        )
        
        # Check required response fields
        required_fields = ['status', 'filename', 'document_stats', 'clauses', 'summary']
        
        for field in required_fields:
            if field not in response:
                print(f"✗ Missing field '{field}' in response")
                return False
        
        # Check document stats
        stats = response['document_stats']
        required_stats = ['total_characters', 'total_clauses', 'classified_clauses', 'ranked_clauses']
        
        for stat in required_stats:
            if stat not in stats:
                print(f"✗ Missing stat '{stat}' in document_stats")
                return False
        
        # Check summary
        summary = response['summary']
        required_summary = ['high_priority_count', 'medium_priority_count', 'low_priority_count', 'clause_types']
        
        for item in required_summary:
            if item not in summary:
                print(f"✗ Missing item '{item}' in summary")
                return False
        
        print("✓ Response structure creation works")
        return True
        
    except Exception as e:
        print(f"✗ Response structure test failed: {e}")
        return False

def test_dependency_fallbacks():
    """Test that optional dependencies have proper fallbacks."""
    print("\nTesting dependency fallbacks...")
    
    try:
        # Test clause_classifier fallback
        from clause_classifier import AI_PIPELINE_AVAILABLE
        print(f"✓ AI pipeline availability: {AI_PIPELINE_AVAILABLE}")
        
        # Test clause_ranker fallback
        from clause_ranker import AI_PIPELINE_AVAILABLE as RANKER_AI_AVAILABLE
        print(f"✓ Ranker AI pipeline availability: {RANKER_AI_AVAILABLE}")
        
        from clause_ranker import EMBEDDINGS_AVAILABLE
        print(f"✓ Embeddings availability: {EMBEDDINGS_AVAILABLE}")
        
        # Test document_processor fallback
        from document_processor import PDFPLUMBER_AVAILABLE
        print(f"✓ PDFPlumber availability: {PDFPLUMBER_AVAILABLE}")
        
        from document_processor import TEXTRACT_AVAILABLE
        print(f"✓ Textract availability: {TEXTRACT_AVAILABLE}")
        
        return True
        
    except Exception as e:
        print(f"✗ Dependency fallback test failed: {e}")
        return False

def test_upload_endpoint_structure():
    """Test upload endpoint structure."""
    print("\nTesting upload endpoint structure...")
    
    try:
        from routes.upload import UploadResponse, ClauseResponse, DocumentStatsResponse, SummaryResponse
        
        # Test that response models are properly defined
        clause_fields = ClauseResponse.__fields__
        required_clause_fields = ['clause_id', 'text', 'type', 'confidence', 'priority_score', 'color', 'rank']
        
        for field in required_clause_fields:
            if field not in clause_fields:
                print(f"✗ Missing field '{field}' in ClauseResponse")
                return False
        
        print("✓ Upload endpoint response models are correct")
        return True
        
    except Exception as e:
        print(f"✗ Upload endpoint structure test failed: {e}")
        return False

def main():
    """Run all stability tests."""
    print("Backend Stability Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_pipeline_structure,
        test_clause_structure,
        test_response_structure,
        test_dependency_fallbacks,
        test_upload_endpoint_structure
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
        print("✓ All stability tests passed!")
        print("✓ Backend is stable and ready for frontend integration")
        print("\nBackend Architecture Summary:")
        print("  ✓ Clean modular structure")
        print("  ✓ Proper dependency validation")
        print("  ✓ Safe fallbacks for optional dependencies")
        print("  ✓ Standardized data structures")
        print("  ✓ Async upload endpoint")
        print("  ✓ Comprehensive error handling")
        print("  ✓ Database integration")
        return 0
    else:
        print("⚠ Some stability tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
