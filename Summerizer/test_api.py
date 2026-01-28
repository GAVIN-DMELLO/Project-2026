"""
API Test Script for Academic Summarizer
This script tests the backend API endpoints to ensure everything is working correctly
"""

import requests
import json

API_BASE = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    print("\n" + "="*50)
    print("Testing Health Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Health check passed!")
            return True
        else:
            print("✗ Health check failed!")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Is it running?")
        print("  Start the server with: python app.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_home():
    """Test the home endpoint"""
    print("\n" + "="*50)
    print("Testing Home Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Home endpoint working!")
            return True
        else:
            print("✗ Home endpoint failed!")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_pdf_upload():
    """Test PDF upload endpoint (without actual file)"""
    print("\n" + "="*50)
    print("Testing PDF Upload Endpoint")
    print("="*50)
    print("Note: This will fail without a real PDF file")
    
    try:
        # Try without file to see error handling
        response = requests.post(f"{API_BASE}/api/summarize-pdf")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400 and "error" in response.json():
            print("✓ Error handling working correctly!")
            return True
        else:
            print("✗ Unexpected response")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_youtube_endpoint():
    """Test YouTube endpoint (with invalid URL)"""
    print("\n" + "="*50)
    print("Testing YouTube Endpoint")
    print("="*50)
    print("Note: Testing with invalid URL to check error handling")
    
    try:
        # Try with invalid URL
        response = requests.post(
            f"{API_BASE}/api/summarize-youtube",
            data={"url": "not-a-valid-url"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400 and "error" in response.json():
            print("✓ Error handling working correctly!")
            return True
        else:
            print("✗ Unexpected response")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Academic Summarizer - API Test Suite")
    print("="*60)
    print("\nMake sure the backend server is running before testing!")
    print("Start it with: python app.py")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nTest cancelled.")
        return
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Home Endpoint", test_home()))
    results.append(("PDF Upload Error Handling", test_pdf_upload()))
    results.append(("YouTube Error Handling", test_youtube_endpoint()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! Your backend is working correctly.")
        print("\nNext steps:")
        print("1. Open frontend/index.html in your browser")
        print("2. Try uploading a PDF or analyzing a YouTube video")
    else:
        print("\n⚠ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("- Make sure the server is running (python app.py)")
        print("- Check if port 5000 is available")
        print("- Verify all dependencies are installed")


if __name__ == "__main__":
    main()
