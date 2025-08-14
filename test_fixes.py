#!/usr/bin/env python3
"""
Test Script - Verify Unit Test Fixes
Test the specific issues that were failing in the unit tests
"""

import requests
import json

def test_missing_json_data():
    """Test that missing JSON data returns 400 (not 500)"""
    print("🧪 Testing Missing JSON Data Fix...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        # Send request with no JSON body (this was causing 500 before)
        response = requests.post(url, headers=headers, timeout=10)
        
        print(f"📥 Status code: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 400:
            data = response.json()
            if data.get("error", {}).get("code") == "MISSING_JSON_DATA":
                print("✅ SUCCESS! Missing JSON data now returns 400 with proper error")
                return True
            else:
                print("❌ Returns 400 but wrong error code")
                return False
        else:
            print(f"❌ Still returning {response.status_code} instead of 400")
            return False
            
    except Exception as e:
        print(f"❌ Error testing missing JSON: {e}")
        return False

def test_datetime_warnings():
    """Test that datetime warnings are fixed"""
    print("\n📅 Testing Datetime Deprecation Fix...")
    
    url = "http://localhost:5000/api/health"
    
    try:
        response = requests.get(url, timeout=5)
        
        print(f"📥 Health check status: {response.status_code}")
        
        if response.status_code in [200, 503]:
            data = response.json()
            timestamp = data.get("timestamp")
            
            if timestamp and "Z" in timestamp:
                print("✅ SUCCESS! Timestamp format is correct")
                print(f"   Timestamp: {timestamp}")
                return True
            else:
                print("❌ Timestamp format issue")
                return False
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing datetime: {e}")
        return False

def test_options_request():
    """Test that OPTIONS requests work (CORS fix)"""
    print("\n🌐 Testing OPTIONS Request Fix...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    
    headers = {
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    try:
        response = requests.options(url, headers=headers, timeout=5)
        
        print(f"📥 OPTIONS status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! OPTIONS requests now work")
            return True
        else:
            print(f"❌ OPTIONS still failing: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing OPTIONS: {e}")
        return False

def test_valid_request():
    """Test that valid requests still work"""
    print("\n✅ Testing Valid Request Still Works...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    data = {"text": "This is a test"}
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        
        print(f"📥 Valid request status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success") and "data" in result:
                print("✅ SUCCESS! Valid requests still work perfectly")
                return True
            else:
                print("❌ Valid request returns 200 but wrong format")
                return False
        else:
            print(f"❌ Valid request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing valid request: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 UNIT TEST FIXES VERIFICATION")
    print("=" * 40)
    
    success_count = 0
    total_tests = 4
    
    # Test 1: Missing JSON data fix
    if test_missing_json_data():
        success_count += 1
    
    # Test 2: Datetime warnings fix
    if test_datetime_warnings():
        success_count += 1
    
    # Test 3: OPTIONS request fix
    if test_options_request():
        success_count += 1
    
    # Test 4: Valid requests still work
    if test_valid_request():
        success_count += 1
    
    print(f"\n📊 RESULTS: {success_count}/{total_tests} fixes verified")
    
    if success_count == total_tests:
        print("🎉 ALL FIXES VERIFIED!")
        print("✅ Missing JSON data returns 400")
        print("✅ Datetime warnings fixed")
        print("✅ OPTIONS requests work")
        print("✅ Valid requests still work")
        print("\n🧪 Run unit tests again:")
        print("   python run_tests.py --fast")
        return True
    else:
        print("⚠️  Some fixes need more work")
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