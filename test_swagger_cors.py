#!/usr/bin/env python3
"""
Test Script - Verify CORS Preflight Fix for Swagger UI
Test that OPTIONS requests are handled properly
"""

import requests
import json

def test_options_request():
    """Test OPTIONS request (CORS preflight)"""
    print("🌐 Testing OPTIONS Request (CORS Preflight)...")
    
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    
    headers = {
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type',
        'Origin': 'http://localhost:5000'
    }
    
    try:
        response = requests.options(url, headers=headers, timeout=5)
        
        print(f"📥 OPTIONS Status: {response.status_code}")
        print(f"📥 OPTIONS Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ OPTIONS request SUCCESS!")
            print("✅ CORS preflight working")
            return True
        else:
            print(f"❌ OPTIONS request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ OPTIONS request error: {e}")
        return False

def test_post_after_options():
    """Test POST request after OPTIONS (simulating Swagger UI)"""
    print("\n📤 Testing POST Request (After OPTIONS)...")
    
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    data = {"problem": "What are 3 benefits of reading?"}
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:5000'
    }
    
    try:
        # First, send OPTIONS request (like Swagger UI does)
        options_response = requests.options(url, headers={
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type',
            'Origin': 'http://localhost:5000'
        })
        
        print(f"📥 Preflight OPTIONS: {options_response.status_code}")
        
        # Then send the actual POST request
        post_response = requests.post(url, json=data, headers=headers, timeout=15)
        
        print(f"📥 POST Status: {post_response.status_code}")
        
        if post_response.status_code == 200:
            result = post_response.json()
            print("✅ POST request SUCCESS!")
            print(f"   Technique: {result.get('data', {}).get('technique', 'unknown')}")
            output = result.get('data', {}).get('output', '')
            print(f"   Output preview: {output[:100]}...")
            return True
        else:
            print(f"❌ POST request failed: {post_response.status_code}")
            print(f"   Response: {post_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ POST request error: {e}")
        return False

def test_multiple_endpoints():
    """Test OPTIONS on multiple endpoints"""
    print("\n🔄 Testing Multiple Endpoints...")
    
    endpoints = [
        "/api/v1/few-shot/sentiment",
        "/api/v1/chain-of-thought/math",
        "/api/v1/tree-of-thought/explore",
        "/api/v1/self-consistency/validate",
        "/api/v1/meta-prompting/optimize"
    ]
    
    success_count = 0
    
    for endpoint in endpoints:
        url = f"http://localhost:5000{endpoint}"
        
        try:
            response = requests.options(url, headers={
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: OPTIONS OK")
                success_count += 1
            else:
                print(f"❌ {endpoint}: OPTIONS failed ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {endpoint}: OPTIONS error ({e})")
    
    print(f"\n📊 OPTIONS Results: {success_count}/{len(endpoints)} endpoints working")
    return success_count == len(endpoints)

def main():
    """Main test function"""
    print("🌐 CORS PREFLIGHT FIX TEST - SWAGGER UI COMPATIBILITY")
    print("=" * 60)
    
    success_count = 0
    total_tests = 3
    
    # Test 1: Basic OPTIONS request
    if test_options_request():
        success_count += 1
    
    # Test 2: POST after OPTIONS (Swagger UI simulation)
    if test_post_after_options():
        success_count += 1
    
    # Test 3: Multiple endpoints
    if test_multiple_endpoints():
        success_count += 1
    
    print(f"\n📊 FINAL RESULTS: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 ALL CORS TESTS PASSED!")
        print("✅ OPTIONS requests working")
        print("✅ CORS preflight fixed")
        print("✅ Swagger UI should work perfectly now")
        print("\n🚀 Try Swagger UI: http://localhost:5000/docs/")
        print("   No more 'Failed to fetch' errors!")
        return True
    else:
        print("⚠️  Some CORS tests failed. Check server logs.")
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