#!/usr/bin/env python3
"""
Quick Test Script for Chain-of-Thought Analysis
Test the fixed endpoint with timeout handling
"""

import requests
import json
import time

def test_chain_of_thought_analysis():
    """Test the chain-of-thought analysis endpoint with timeout handling"""
    print("🔗 Testing Chain-of-Thought Analysis (with timeout fix)...")
    
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    
    # Test with a simpler problem first
    simple_data = {"problem": "What are 3 benefits of exercise?"}
    
    print(f"📤 Testing with simple problem: {simple_data['problem']}")
    
    try:
        start_time = time.time()
        response = requests.post(
            url, 
            json=simple_data, 
            headers={'Content-Type': 'application/json'},
            timeout=25  # 25 second timeout
        )
        end_time = time.time()
        
        print(f"📥 Response time: {end_time - start_time:.2f} seconds")
        print(f"📥 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"   Technique: {result.get('data', {}).get('technique', 'unknown')}")
            print(f"   Task: {result.get('data', {}).get('task', 'unknown')}")
            output = result.get('data', {}).get('output', '')
            print(f"   Output preview: {output[:200]}...")
            
            # Now test with the original complex problem
            print("\n🔗 Testing with complex problem...")
            complex_data = {"problem": "What are the potential impacts of AI on employment?"}
            
            start_time = time.time()
            response = requests.post(
                url, 
                json=complex_data, 
                headers={'Content-Type': 'application/json'},
                timeout=25
            )
            end_time = time.time()
            
            print(f"📥 Complex response time: {end_time - start_time:.2f} seconds")
            print(f"📥 Complex status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ COMPLEX ANALYSIS SUCCESS!")
                output = result.get('data', {}).get('output', '')
                print(f"   Output preview: {output[:200]}...")
                return True
            else:
                print(f"❌ Complex analysis failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        else:
            print(f"❌ Simple test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (even with 25s timeout)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_swagger_ui_compatibility():
    """Test if the endpoint works from Swagger UI perspective"""
    print("\n🌐 Testing Swagger UI Compatibility...")
    
    # Test the exact same request that Swagger UI would make
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    data = {"problem": "What are the potential impacts of AI on employment?"}
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        print("📤 Making Swagger UI compatible request...")
        response = requests.post(url, json=data, headers=headers, timeout=25)
        
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Swagger UI compatible request SUCCESS!")
            return True
        else:
            print(f"❌ Swagger UI compatible request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Swagger UI compatibility test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 QUICK TEST - CHAIN-OF-THOUGHT ANALYSIS WITH TIMEOUT FIX")
    print("=" * 60)
    
    # Test 1: Basic functionality
    if not test_chain_of_thought_analysis():
        print("\n💡 The endpoint is still having issues. Check server logs.")
        return False
    
    # Test 2: Swagger UI compatibility
    if not test_swagger_ui_compatibility():
        print("\n💡 The endpoint works with curl but not Swagger UI. Check CORS settings.")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("The endpoint should now work in both curl and Swagger UI!")
    print("\n📚 Try it in Swagger UI: http://localhost:5000/docs/")
    return True

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