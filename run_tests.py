#!/usr/bin/env python3
"""
Test Runner for Local Advanced Prompting System Flask API
Comprehensive test runner with server management and multiple test options
"""

import os
import sys
import argparse
import subprocess
import time
import requests
from pathlib import Path


def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking Environment Setup...")
    
    issues = []
    
    # Check .env file
    if not os.path.exists('.env'):
        issues.append("❌ .env file not found")
    else:
        print("✅ .env file found")
    
    # Check API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        issues.append("❌ GEMINI_API_KEY not set in environment")
    elif len(api_key) < 20:
        issues.append("⚠️  GEMINI_API_KEY seems too short")
    else:
        print("✅ GEMINI_API_KEY configured")
    
    # Check required modules
    required_modules = ['flask', 'google.genai', 'dotenv', 'pytest', 'requests']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} available")
        except ImportError:
            issues.append(f"❌ {module} not installed")
    
    return issues


def run_quick_test():
    """Run a quick smoke test"""
    print("\n🚀 Running Quick Smoke Test...")
    
    try:
        # Test Flask app creation
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code in [200, 503]:
                print("✅ Flask app creation successful")
                print("✅ Health endpoint accessible")
                return True
            else:
                print(f"❌ Health endpoint returned {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False


def run_pytest_tests(test_type="fast", verbose=True, failfast=False):
    """Run pytest tests"""
    print(f"\n🧪 Running {test_type.upper()} Tests with Pytest...")
    
    # Prepare pytest command
    cmd = [sys.executable, "-m", "pytest", "tests/test_api.py"]
    
    if verbose:
        cmd.append("-v")
    
    if failfast:
        cmd.append("-x")
    
    # Add markers based on test type
    if test_type == "fast":
        cmd.extend(["-m", "not slow"])
    elif test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    
    # Add coverage if available
    try:
        import coverage
        cmd.extend(["--cov=.", "--cov-report=term-missing"])
    except ImportError:
        pass
    
    # Run tests
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run pytest: {e}")
        return False


def run_specific_test(test_name):
    """Run a specific test case"""
    print(f"\n🎯 Running Specific Test: {test_name}")
    
    # Map friendly names to actual test methods
    test_mapping = {
        "health": "test_api.py::TestAPIHealth",
        "few-shot": "test_api.py::TestFewShotEndpoints",
        "chain-of-thought": "test_api.py::TestChainOfThoughtEndpoints",
        "tree-of-thought": "test_api.py::TestTreeOfThoughtEndpoints",
        "self-consistency": "test_api.py::TestSelfConsistencyEndpoints",
        "meta-prompting": "test_api.py::TestMetaPromptingEndpoints",
        "errors": "test_api.py::TestErrorHandling",
        "performance": "test_api.py::TestPerformance"
    }
    
    test_path = test_mapping.get(test_name, f"test_api.py::{test_name}")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        f"tests/{test_path}",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run specific test: {e}")
        return False


def test_live_server():
    """Test with a live server instance"""
    print("\n🌐 Testing with Live Server...")
    
    try:
        # Start server in background
        from app import create_app
        import threading
        
        app = create_app()
        server_thread = threading.Thread(
            target=lambda: app.run(host='127.0.0.1', port=5002, debug=False),
            daemon=True
        )
        server_thread.start()
        
        # Wait for server to start
        time.sleep(2)
        
        # Test endpoints
        base_url = "http://127.0.0.1:5002"
        
        # Test health
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code in [200, 503]:
            print("✅ Live server health check passed")
        else:
            print(f"❌ Live server health check failed: {response.status_code}")
            return False
        
        # Test a simple endpoint
        test_data = {"text": "This is a test"}
        response = requests.post(
            f"{base_url}/api/v1/few-shot/sentiment",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Live server API test passed")
            return True
        else:
            print(f"❌ Live server API test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Live server test failed: {e}")
        return False


def run_performance_benchmark():
    """Run performance benchmark"""
    print("\n⚡ Running Performance Benchmark...")
    
    try:
        # Run performance tests specifically
        cmd = [
            sys.executable, "-m", "pytest", 
            "tests/test_api.py::TestPerformance",
            "-v", "--tb=short"
        ]
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(
        description="Test Runner for Local Advanced Prompting System Flask API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run environment check + fast tests
  python run_tests.py --fast             # Run fast tests with mocks (~15s)
  python run_tests.py --full             # Run all tests including slow ones
  python run_tests.py --quick            # Run quick smoke test only (~5s)
  python run_tests.py --check            # Check environment setup only
  python run_tests.py --test few-shot    # Run specific test category
  python run_tests.py --live             # Test with live server
  python run_tests.py --benchmark        # Run performance benchmark
        """
    )
    
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Run quick smoke test only"
    )
    
    parser.add_argument(
        "--fast", "-f",
        action="store_true",
        help="Run fast tests with mocked API calls (~15 seconds)"
    )
    
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run all tests including slow ones (~60+ seconds)"
    )
    
    parser.add_argument(
        "--check", "-c",
        action="store_true", 
        help="Check environment setup only"
    )
    
    parser.add_argument(
        "--test", "-t",
        choices=["health", "few-shot", "chain-of-thought", "tree-of-thought", 
                "self-consistency", "meta-prompting", "errors", "performance"],
        help="Run a specific test category"
    )
    
    parser.add_argument(
        "--live", "-l",
        action="store_true",
        help="Test with live server instance"
    )
    
    parser.add_argument(
        "--benchmark", "-b",
        action="store_true",
        help="Run performance benchmark"
    )
    
    parser.add_argument(
        "--failfast",
        action="store_true",
        help="Stop on first test failure"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=True,
        help="Verbose output (default: True)"
    )
    
    args = parser.parse_args()
    
    print("🧪 LOCAL ADVANCED PROMPTING SYSTEM - API TEST RUNNER")
    print("=" * 70)
    
    # Always check environment first
    issues = check_environment()
    
    if issues:
        print(f"\n⚠️  Environment Issues Found ({len(issues)}):")
        for issue in issues:
            print(f"   {issue}")
        
        if not args.check:
            print("\n💡 Fix these issues before running tests:")
            print("   1. Create .env file: cp .env.example .env")
            print("   2. Add your API key to .env file")
            print("   3. Install dependencies: pip install -r requirements.txt")
        
        if "GEMINI_API_KEY" in str(issues):
            return 1
    
    if args.check:
        print(f"\n✅ Environment check complete - {len(issues)} issues found")
        return 0 if len(issues) == 0 else 1
    
    # Run tests based on arguments
    success = True
    
    if args.quick:
        success = run_quick_test()
    elif args.fast:
        success = run_pytest_tests("fast", args.verbose, args.failfast)
    elif args.full:
        success = run_pytest_tests("full", args.verbose, args.failfast)
    elif args.test:
        success = run_specific_test(args.test)
    elif args.live:
        success = test_live_server()
    elif args.benchmark:
        success = run_performance_benchmark()
    else:
        # Default: Run quick test first, then fast tests
        if run_quick_test():
            print("\n💡 Running FAST tests by default (use --full for complete suite)")
            success = run_pytest_tests("fast", args.verbose, args.failfast)
        else:
            print("❌ Quick test failed - skipping test suite")
            success = False
    
    # Final summary
    print("\n" + "=" * 70)
    if success:
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("Your Local Advanced Prompting System API is working correctly.")
    else:
        print("❌ SOME TESTS FAILED")
        print("Check the output above for details on what needs to be fixed.")
    
    print("=" * 70)
    return 0 if success else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Test runner interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        sys.exit(1)