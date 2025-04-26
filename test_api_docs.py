"""
Test script to verify API documentation endpoints
"""
import requests
import time
import json

# Allow the server some time to start up fully
print("Waiting for server to fully start...")
time.sleep(5)

# Base URL for testing
BASE_URL = "http://localhost:8000"

# URLs to test
test_urls = [
    "/",
    "/api",
    "/docs",
    "/redoc",
    "/swagger-ui",
    "/openapi.json"
]

# Keep track of all test results
results = {}

# Test each URL
for url in test_urls:
    try:
        full_url = f"{BASE_URL}{url}"
        print(f"Testing {full_url}...")
        response = requests.get(full_url)
        status = response.status_code
        results[url] = status
        if status == 200:
            print(f"✅ {url} - Status: {status}")
        else:
            print(f"❌ {url} - Status: {status}")
    except Exception as e:
        results[url] = f"Error: {str(e)}"
        print(f"❌ {url} - Error: {str(e)}")

# Specific test for OpenAPI schema validation
try:
    print("\nValidating OpenAPI schema...")
    openapi_url = f"{BASE_URL}/openapi.json"
    response = requests.get(openapi_url)
    if response.status_code == 200:
        schema = response.json()
        # Check for required OpenAPI fields
        required_fields = ["openapi", "info", "paths"]
        missing_fields = [field for field in required_fields if field not in schema]
        
        if not missing_fields:
            print("✅ OpenAPI schema validation passed")
            
            # Check for code samples
            if "components" in schema and "schemas" in schema["components"]:
                paths = schema.get("paths", {})
                generate_path = paths.get("/api/v1/generate/", {})
                post_method = generate_path.get("post", {})
                
                if "x-codeSamples" in post_method:
                    print("✅ Code samples validation passed")
                else:
                    print("❌ Code samples missing from OpenAPI schema")
        else:
            print(f"❌ OpenAPI schema missing required fields: {', '.join(missing_fields)}")
    else:
        print(f"❌ OpenAPI schema validation failed: {response.status_code}")
except Exception as e:
    print(f"❌ OpenAPI schema validation error: {str(e)}")

# Print summary
print("\nAPI Documentation Test Summary:")
print("-" * 50)
all_passed = True
for url, status in results.items():
    if status == 200:
        print(f"✅ {url} - Passed")
    else:
        all_passed = False
        print(f"❌ {url} - Failed: {status}")

# Final result
if all_passed:
    print("\n🎉 All API documentation endpoints are working correctly!")
else:
    print("\n⚠️ Some API documentation endpoints failed. Check the logs for details.") 