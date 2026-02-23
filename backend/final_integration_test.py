"""
Final Integration Test - Complete System Validation

Tests the entire LexAI backend system with all upgraded components:
- Environment configuration
- Constitution matching
- Multi-model generative service
- Performance optimization
- Document analysis pipeline
- Chatbot infrastructure
"""

import sys
import os
import json
import asyncio
from datetime import datetime

# Add paths
sys.path.append('ai')
sys.path.append('services')
sys.path.append('routes')

from dotenv import load_dotenv
load_dotenv()

# Import all components
from ai.constitution_matcher import ConstitutionMatcher
from ai.generative_service import GenerativeService, generate_full_clause_analysis
from ai.performance_optimizer import get_performance_optimizer
from services.document_analysis_service import DocumentAnalysisService
from ai.chatbot_service import get_chatbot_service

class IntegrationTestSuite:
    """Comprehensive integration test suite."""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"   {status} {test_name}")
        if details:
            print(f"      {details}")
    
    def test_environment_configuration(self):
        """Test environment configuration and API keys."""
        print("\n🔍 Testing Environment Configuration...")
        
        # Test API key
        api_key = os.getenv('OPENROUTER_API_KEY')
        self.log_test(
            "API Key Available", 
            bool(api_key),
            f"Key length: {len(api_key) if api_key else 0}"
        )
        
        # Test .env file
        env_file_exists = os.path.exists('.env')
        self.log_test(
            ".env File Exists",
            env_file_exists
        )
        
        # Test data directory
        data_dir_exists = os.path.exists('data')
        self.log_test(
            "Data Directory Exists",
            data_dir_exists
        )
        
        # Test constitution files
        constitution_files = ['COI.json', 'China_2018.json', 'Japan_1946.json', 'Russia_2014.json']
        for file in constitution_files:
            file_path = os.path.join('data', file)
            self.log_test(
                f"Constitution File: {file}",
                os.path.exists(file_path)
            )
    
    def test_constitution_matcher(self):
        """Test constitution matching functionality."""
        print("\n🔍 Testing Constitution Matcher...")
        
        try:
            matcher = ConstitutionMatcher()
            self.log_test("Constitution Matcher Initialized", True)
            
            # Test loading constitutions
            loaded = matcher.load_constitutions()
            self.log_test("Constitutions Loaded", loaded)
            
            # Test matching
            test_clause = "All citizens shall have the right to freedom of speech"
            matches = matcher.match_constitution_sections(test_clause, "US", top_k=3)
            self.log_test(
                "Constitution Matching",
                len(matches) > 0,
                f"Found {len(matches)} matches"
            )
            
        except Exception as e:
            self.log_test("Constitution Matcher", False, str(e))
    
    def test_generative_service(self):
        """Test multi-model generative service."""
        print("\n🔍 Testing Generative Service...")
        
        try:
            service = GenerativeService()
            self.log_test("Generative Service Initialized", True)
            self.log_test("API Available", service.api_available)
            self.log_test("API Validated", service.api_validated)
            
            if service.api_available:
                # Test comprehensive analysis
                test_clause = "All parties shall maintain confidentiality of shared information"
                analysis = generate_full_clause_analysis(
                    test_clause,
                    "US Constitution",
                    "confidentiality"
                )
                
                self.log_test(
                    "Comprehensive Analysis",
                    bool(analysis),
                    f"Explanation length: {len(analysis.get('explanation', ''))}"
                )
                
                # Test risk assessment
                risk_level = analysis.get('risk_level', 'unknown')
                self.log_test(
                    "Risk Assessment",
                    risk_level in ['high', 'medium', 'low'],
                    f"Risk level: {risk_level}"
                )
            
        except Exception as e:
            self.log_test("Generative Service", False, str(e))
    
    def test_performance_optimization(self):
        """Test performance optimization features."""
        print("\n🔍 Testing Performance Optimization...")
        
        try:
            optimizer = get_performance_optimizer()
            self.log_test("Performance Optimizer Initialized", True)
            
            # Test embedding caching
            test_text = "Test clause for caching"
            cached_embedding = optimizer.get_cached_embedding(test_text)
            self.log_test("Initial Cache Check", not cached_embedding)
            
            # Cache embedding
            test_embedding = [0.1, 0.2, 0.3]
            optimizer.cache_embedding(test_text, test_embedding)
            
            # Test cache retrieval
            cached_embedding = optimizer.get_cached_embedding(test_text)
            self.log_test("Embedding Caching", bool(cached_embedding))
            
            # Test performance stats
            stats = optimizer.get_performance_stats()
            self.log_test(
                "Performance Statistics",
                'cache_hits' in stats,
                f"Hit rate: {stats.get('hit_rate_percent', 0)}%"
            )
            
        except Exception as e:
            self.log_test("Performance Optimization", False, str(e))
    
    def test_document_analysis_pipeline(self):
        """Test complete document analysis pipeline."""
        print("\n🔍 Testing Document Analysis Pipeline...")
        
        try:
            service = DocumentAnalysisService()
            self.log_test("Document Analysis Service Initialized", True)
            
            # Test with sample document
            sample_text = """
            This agreement is made on January 1, 2024.
            
            1. All parties shall have the right to freedom of speech.
            2. No person shall be deprived of property without due process.
            3. Confidential information must be protected.
            """
            
            # Create mock file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(sample_text)
                temp_file = f.name
            
            # Test analysis
            from fastapi import UploadFile
            with open(temp_file, 'rb') as f:
                upload_file = UploadFile(filename="test.txt", file=f)
                
                # Run analysis
                result = asyncio.run(service.analyze_document(upload_file, "US Constitution"))
            
            # Clean up
            os.unlink(temp_file)
            
            self.log_test(
                "Document Analysis Completed",
                result.get('status') == 'success',
                f"Clauses found: {len(result.get('clauses', []))}"
            )
            
            # Test comprehensive analysis in clauses
            if result.get('clauses'):
                first_clause = result['clauses'][0]
                has_comprehensive = (
                    first_clause.get('explanation') and
                    first_clause.get('offensive_analysis') and
                    first_clause.get('defensive_analysis')
                )
                self.log_test(
                    "Comprehensive Clause Analysis",
                    has_comprehensive,
                    f"Risk level: {first_clause.get('risk_level', 'unknown')}"
                )
            
        except Exception as e:
            self.log_test("Document Analysis Pipeline", False, str(e))
    
    def test_chatbot_infrastructure(self):
        """Test chatbot infrastructure."""
        print("\n🔍 Testing Chatbot Infrastructure...")
        
        try:
            chatbot = get_chatbot_service()
            self.log_test("Chatbot Service Initialized", True)
            
            # Test session creation
            sample_clauses = [
                {
                    "text": "Test clause 1",
                    "type": "test",
                    "risk_level": "low"
                }
            ]
            
            session_id = chatbot.create_session(
                document_text="Test document",
                constitution="US Constitution",
                clauses=sample_clauses
            )
            self.log_test("Session Creation", bool(session_id))
            
            # Test message handling
            chatbot.add_message(session_id, "user", "Test message")
            history = chatbot.get_conversation_history(session_id)
            self.log_test(
                "Message Handling",
                len(history) > 0,
                f"Messages: {len(history)}"
            )
            
            # Test document summary
            summary = chatbot.get_document_summary(session_id)
            self.log_test(
                "Document Summary",
                'document_info' in summary,
                f"Clauses: {summary.get('document_info', {}).get('total_clauses', 0)}"
            )
            
            # Test session cleanup
            chatbot.clear_session(session_id)
            self.log_test("Session Cleanup", True)
            
        except Exception as e:
            self.log_test("Chatbot Infrastructure", False, str(e))
    
    def test_api_endpoints(self):
        """Test API endpoint availability."""
        print("\n🔍 Testing API Endpoints...")
        
        try:
            # Test main app import
            from main import app
            self.log_test("Main App Import", True)
            
            # Test router imports
            from routes.upload import router as upload_router
            self.log_test("Upload Router", True)
            
            from routes.chatbot import router as chatbot_router
            self.log_test("Chatbot Router", True)
            
            # Test app configuration
            self.log_test(
                "App Configuration",
                app.title == "Legal AI API",
                f"Title: {app.title}"
            )
            
        except Exception as e:
            self.log_test("API Endpoints", False, str(e))
    
    def run_all_tests(self):
        """Run all integration tests."""
        print("🚀 Starting LexAI Backend Integration Tests")
        print("=" * 50)
        
        # Run all test suites
        self.test_environment_configuration()
        self.test_constitution_matcher()
        self.test_generative_service()
        self.test_performance_optimization()
        self.test_document_analysis_pipeline()
        self.test_chatbot_infrastructure()
        self.test_api_endpoints()
        
        # Generate final report
        self.generate_final_report()
    
    def generate_final_report(self):
        """Generate final integration test report."""
        print("\n" + "=" * 50)
        print("📊 FINAL INTEGRATION TEST REPORT")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if "PASS" in r['status']])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        print(f"\nTest Duration: {datetime.now() - self.start_time}")
        
        # Show failed tests
        failed_tests_list = [r for r in self.test_results if "FAIL" in r['status']]
        if failed_tests_list:
            print("\n❌ Failed Tests:")
            for test in failed_tests_list:
                print(f"   - {test['test']}: {test['details']}")
        
        # Overall status
        if success_rate >= 90:
            print("\n🎉 INTEGRATION TESTS: EXCELLENT")
        elif success_rate >= 75:
            print("\n✅ INTEGRATION TESTS: GOOD")
        elif success_rate >= 50:
            print("\n⚠️  INTEGRATION TESTS: ACCEPTABLE")
        else:
            print("\n❌ INTEGRATION TESTS: NEEDS ATTENTION")
        
        # Save report
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": success_rate,
                "duration": str(datetime.now() - self.start_time)
            },
            "tests": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        with open('integration_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: integration_test_report.json")

# Run integration tests
if __name__ == "__main__":
    test_suite = IntegrationTestSuite()
    test_suite.run_all_tests()
