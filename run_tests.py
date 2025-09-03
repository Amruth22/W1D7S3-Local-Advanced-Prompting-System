#!/usr/bin/env python3
"""
Test Runner for Local Advanced Prompting System
Provides multiple test execution modes for different use cases
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def print_banner():
    """Print test runner banner"""
    print("=" * 70)
    print("🧪 LOCAL ADVANCED PROMPTING SYSTEM - TEST RUNNER")
    print("=" * 70)

def check_environment():
    """Check environment setup"""
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or not api_key.startswith('AIza'):
        print("❌ GEMINI_API_KEY not found or invalid!")
        print("\n📋 Setup Instructions:")
        print("1. Copy .env.example to .env: cp .env.example .env")
        print("2. Get API key: https://makersuite.google.com/app/apikey")
        print("3. Add to .env: GEMINI_API_KEY=your-api-key-here")
        return False
    
    print(f"✅ API Key configured: {api_key[:10]}...{api_key[-5:]}")
    return True

def run_quick_tests():
    """Run quick tests with optimized performance"""
    print("\n🚀 QUICK TEST MODE")
    print("- Reduced API calls for faster execution")
    print("- Essential component validation")
    print("- Expected time: ~10-15 seconds")
    print("-" * 50)
    
    # Set environment variable for quick mode
    env = os.environ.copy()
    env['QUICK_TEST_MODE'] = 'true'
    env['MAX_API_CALLS_PER_TEST'] = '1'
    env['API_TIMEOUT'] = '10'
    
    start_time = time.time()
    result = subprocess.run([sys.executable, 'test_unit.py'], env=env)
    total_time = time.time() - start_time
    
    print(f"\n⏱️  Quick tests completed in {total_time:.2f} seconds")
    return result.returncode == 0

def run_full_tests():
    """Run comprehensive tests with full API integration"""
    print("\n🔬 FULL TEST MODE")
    print("- Comprehensive API integration testing")
    print("- All advanced prompting techniques")
    print("- Expected time: ~45-60 seconds")
    print("-" * 50)
    
    # Set environment variable for full mode
    env = os.environ.copy()
    env['QUICK_TEST_MODE'] = 'false'
    env['MAX_API_CALLS_PER_TEST'] = '3'
    env['API_TIMEOUT'] = '30'
    
    start_time = time.time()
    result = subprocess.run([sys.executable, 'test_unit.py'], env=env)
    total_time = time.time() - start_time
    
    print(f"\n⏱️  Full tests completed in {total_time:.2f} seconds")
    return result.returncode == 0

def run_legacy_tests():
    """Run legacy comprehensive tests (if available)"""
    if os.path.exists('tests.py'):
        print("\n📚 LEGACY TEST MODE")
        print("- Comprehensive mocked tests")
        print("- No API calls required")
        print("- Expected time: ~15-20 seconds")
        print("-" * 50)
        
        start_time = time.time()
        result = subprocess.run([sys.executable, 'tests.py'])
        total_time = time.time() - start_time
        
        print(f"\n⏱️  Legacy tests completed in {total_time:.2f} seconds")
        return result.returncode == 0
    else:
        print("❌ Legacy tests (tests.py) not found")
        return False

def run_specific_test(test_name):
    """Run a specific test"""
    print(f"\n🎯 SPECIFIC TEST: {test_name}")
    print("-" * 50)
    
    env = os.environ.copy()
    env['QUICK_TEST_MODE'] = 'true'  # Use quick mode for specific tests
    
    cmd = [
        sys.executable, '-m', 'unittest', 
        f'test_unit.CoreAdvancedPromptingTests.{test_name}', 
        '-v'
    ]
    
    start_time = time.time()
    result = subprocess.run(cmd, env=env)
    total_time = time.time() - start_time
    
    print(f"\n⏱️  Test {test_name} completed in {total_time:.2f} seconds")
    return result.returncode == 0

def show_usage():
    """Show usage instructions"""
    print("\n📖 USAGE:")
    print("python run_tests.py [mode]")
    print("\n🎯 Available modes:")
    print("  quick     - Fast validation (~10-15s)")
    print("  full      - Comprehensive testing (~45-60s)")
    print("  legacy    - Mocked tests (no API calls)")
    print("  specific  - Run specific test")
    print("\n💡 Examples:")
    print("  python run_tests.py quick")
    print("  python run_tests.py full")
    print("  python run_tests.py specific test_01_gemini_client_integration")
    print("\n🔧 Environment Variables:")
    print("  QUICK_TEST_MODE=true/false")
    print("  MAX_API_CALLS_PER_TEST=1-5")
    print("  API_TIMEOUT=10-30")

def main():
    """Main test runner function"""
    print_banner()
    
    # Check environment
    if not check_environment():
        return False
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        show_usage()
        return False
    
    mode = sys.argv[1].lower()
    
    if mode == 'quick':
        return run_quick_tests()
    elif mode == 'full':
        return run_full_tests()
    elif mode == 'legacy':
        return run_legacy_tests()
    elif mode == 'specific':
        if len(sys.argv) < 3:
            print("❌ Please specify test name for specific mode")
            print("Example: python run_tests.py specific test_01_gemini_client_integration")
            return False
        return run_specific_test(sys.argv[2])
    else:
        print(f"❌ Unknown mode: {mode}")
        show_usage()
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Tests completed successfully!")
        else:
            print("\n❌ Tests failed or incomplete")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        sys.exit(1)