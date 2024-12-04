import requests
import json

try:
    response = requests.post(
        "http://localhost:5000/query",
        json={
            "text": "que es jph lions",
            "user_id": "test_user"
        },
        timeout=10
    )
    
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    
    try:
        response_json = response.json()
        print("Parsed Response:")
        print(json.dumps(response_json, indent=2))
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON")
        print("Raw Response:", response.text)

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the server. Are all services running?")
except requests.exceptions.Timeout:
    print("Error: Request timed out")
except Exception as e:
    print(f"Unexpected error: {e}")