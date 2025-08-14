#!/usr/bin/env python3
"""
Endpoint Testing Script
Test individual endpoints to troubleshoot issues
"""

import requests
import json
import time
import sys

def test_server_health():
    """Test if the server is running and healthy"""
    print("🔍 Testing Server Health...")
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('data', {}).get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running on localhost:5000?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_simple_endpoint():
    """Test a simple endpoint first"""
    print("\n🧪 Testing Simple Endpoint (Few-shot Sentiment)...")
    
    url = "http://localhost:5000/api/v1/few-shot/sentiment"
    data = {"text": "This is a test"}
    
    try:
        response = requests.post(
            url, 
            json=data, 
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"✅ Simple endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result.get('success', False)}")
            return True
        else:
            print(f"❌ Simple endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Simple endpoint error: {e}")
        return False

def test_chain_of_thought_analysis():
    """Test the specific chain-of-thought analysis endpoint"""
    print("\n🔗 Testing Chain-of-Thought Analysis Endpoint...")
    
    url = "http://localhost:5000/api/v1/chain-of-thought/analysis"
    data = {"problem": "What are the potential impacts of AI on employment?"}
    
    try:
        print(f"📤 Sending request to: {url}")
        print(f"📤 Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(
            url, 
            json=data, 
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=30  # Longer timeout for complex analysis
        )
        
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chain-of-thought analysis successful!")
            print(f"   Technique: {result.get('data', {}).get('technique', 'unknown')}")
            print(f"   Task: {result.get('data', {}).get('task', 'unknown')}")
            output = result.get('data', {}).get('output', '')
            print(f"   Output preview: {output[:100]}...")
            return True
        else:
            print(f"❌ Chain-of-thought analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The analysis might take longer than expected.")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check if server is running.")
        return False
    except Exception as e:
        print(f"❌ Chain-of-thought analysis error: {e}")
        return False

def test_with_curl_equivalent():
    """Test with the exact curl command equivalent"""
    print("\n🌐 Testing with Curl Equivalent...")
    
    import subprocess
    
    curl_command = [
        'curl', '-X', 'POST',
        'http://localhost:5000/api/v1/chain-of-thought/analysis',
        '-H', 'accept: application/json',
        '-H', 'Content-Type: application/json',
        '-d', '{"problem": "What are the potential impacts of AI on employment?"}',
        '--max-time', '30',
        '-v'  # Verbose output
    ]
    
    try:
        print(f"📤 Running: {' '.join(curl_command)}")
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=35)
        
        print(f"📥 Curl exit code: {result.returncode}")
        if result.stdout:
            print(f"📥 Curl stdout: {result.stdout}")
        if result.stderr:
            print(f"📥 Curl stderr: {result.stderr}")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Curl command timed out")
        return False
    except FileNotFoundError:
        print("❌ Curl not found. Skipping curl test.")
        return False
    except Exception as e:
        print(f"❌ Curl test error: {e}")
        return False

def check_environment():
    """Check environment setup"""
    print("\n🔧 Checking Environment...")
    
    # Check if .env file exists
    import os
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Check if API key is set
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print("✅ GEMINI_API_KEY is set")
        else:
            print("❌ GEMINI_API_KEY not found in .env")
            return False
    else:
        print("❌ .env file not found")
        return False
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000/", timeout=2)
        print("✅ Server is responding")
        return True
    except:
        print("❌ Server is not responding")
        return False

def main():
    """Main testing function"""
    print("🧪 ENDPOINT TROUBLESHOOTING SCRIPT")
    print("=" * 50)
    
    # Step 1: Check environment
    if not check_environment():
        print("\n💡 SOLUTION: Make sure your server is running with 'python app.py'")
        return False
    
    # Step 2: Test server health
    if not test_server_health():
        print("\n💡 SOLUTION: Check server logs for errors")
        return False
    
    # Step 3: Test simple endpoint
    if not test_simple_endpoint():
        print("\n💡 SOLUTION: Check your Gemini API key configuration")
        return False
    
    # Step 4: Test the specific endpoint
    if not test_chain_of_thought_analysis():
        print("\n💡 SOLUTION: The endpoint might be taking too long or there's an API issue")
        return False
    
    # Step 5: Test with curl equivalent
    test_with_curl_equivalent()
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your endpoint should be working correctly.")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        sys.exit(1)