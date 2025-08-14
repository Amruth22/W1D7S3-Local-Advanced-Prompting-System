#!/usr/bin/env python3
"""
Test Script - Specific JSON Handling Fix
Test different scenarios for missing/invalid JSON data
"""

import requests
import json

def test_no_body():
    """Test request with no body at all"""
    print("🧪 Testing No Body...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, timeout=10)
        print(f"📥 No body - Status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_empty_body():
    """Test request with empty body"""
    print("\n🧪 Testing Empty Body...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data="", timeout=10)
        print(f"📥 Empty body - Status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_json():
    """Test request with invalid JSON"""
    print("\n🧪 Testing Invalid JSON...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data="invalid json", timeout=10)
        print(f"📥 Invalid JSON - Status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_empty_json():
    """Test request with empty JSON object"""
    print("\n🧪 Testing Empty JSON Object...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)
        print(f"📥 Empty JSON - Status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_valid_json():
    """Test request with valid JSON"""
    print("\n🧪 Testing Valid JSON...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json={"text": "test"}, timeout=15)
        print(f"📥 Valid JSON - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"📥 Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 JSON HANDLING FIX TEST")
    print("=" * 30)
    
    tests = [
        ("No Body", test_no_body),
        ("Empty Body", test_empty_body),
        ("Invalid JSON", test_invalid_json),
        ("Empty JSON Object", test_empty_json),
        ("Valid JSON", test_valid_json)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            print(f"✅ {test_name} - PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} - FAILED")
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL JSON HANDLING TESTS PASSED!")
        return True
    else:
        print("⚠️  Some JSON handling tests failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)