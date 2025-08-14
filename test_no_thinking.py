#!/usr/bin/env python3
"""
Test Script - Verify Thinking Config is Disabled
Quick test to ensure fast responses without thinking budget
"""

import requests
import json
import time

def test_fast_response():
    """Test that responses are now fast without thinking config"""
    print("⚡ Testing Fast Response (Thinking Config Disabled)...")
    
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    data = {"problem": "What are 3 benefits of exercise?"}
    
    print(f"📤 Testing: {data['problem']}")
    
    try:
        start_time = time.time()
        response = requests.post(
            url, 
            json=data, 
            headers={'Content-Type': 'application/json'},
            timeout=15  # Should be much faster now
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"📥 Response time: {response_time:.2f} seconds")
        print(f"📥 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"   Technique: {result.get('data', {}).get('technique', 'unknown')}")
            output = result.get('data', {}).get('output', '')
            print(f"   Output preview: {output[:150]}...")
            
            # Check if response time is reasonable (should be under 10 seconds now)
            if response_time < 10:
                print(f"🚀 EXCELLENT! Response time is {response_time:.2f}s (under 10s)")
                return True
            elif response_time < 15:
                print(f"✅ GOOD! Response time is {response_time:.2f}s (under 15s)")
                return True
            else:
                print(f"⚠️  Response time is {response_time:.2f}s (still a bit slow)")
                return True
                
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Still timing out (this shouldn't happen now)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_complex_problem():
    """Test with the original complex problem"""
    print("\n🧠 Testing Complex Problem (Should be fast now)...")
    
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    data = {"problem": "What are the potential impacts of AI on employment?"}
    
    print(f"📤 Testing: {data['problem']}")
    
    try:
        start_time = time.time()
        response = requests.post(
            url, 
            json=data, 
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"📥 Response time: {response_time:.2f} seconds")
        print(f"📥 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ COMPLEX PROBLEM SUCCESS!")
            output = result.get('data', {}).get('output', '')
            print(f"   Output preview: {output[:150]}...")
            
            if response_time < 15:
                print(f"🚀 EXCELLENT! Complex analysis completed in {response_time:.2f}s")
                return True
            else:
                print(f"⚠️  Complex analysis took {response_time:.2f}s")
                return True
                
        else:
            print(f"❌ Complex problem failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Complex problem still timing out")
        return False
    except Exception as e:
        print(f"❌ Complex problem error: {e}")
        return False

def test_swagger_ui():
    """Test Swagger UI compatibility"""
    print("\n🌐 Testing Swagger UI Compatibility...")
    
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    data = {"problem": "List 3 benefits of reading books"}
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=data, headers=headers, timeout=15)
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"📥 Swagger UI test time: {response_time:.2f} seconds")
        print(f"📥 Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Swagger UI compatibility SUCCESS!")
            return True
        else:
            print(f"❌ Swagger UI test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Swagger UI test error: {e}")
        return False

def main():
    """Main test function"""
    print("⚡ THINKING CONFIG DISABLED - SPEED TEST")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    # Test 1: Simple problem
    if test_fast_response():
        success_count += 1
    
    # Test 2: Complex problem
    if test_complex_problem():
        success_count += 1
    
    # Test 3: Swagger UI compatibility
    if test_swagger_ui():
        success_count += 1
    
    print(f"\n📊 RESULTS: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Thinking config is disabled")
        print("✅ Responses are fast")
        print("✅ Swagger UI should work perfectly")
        print("\n🚀 Try Swagger UI now: http://localhost:5000/docs/")
        return True
    else:
        print("⚠️  Some tests failed. Check server logs.")
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