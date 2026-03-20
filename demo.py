import time
import hmac
import hashlib
import json
import requests

API_KEY = "dev-api-key"
API_SECRET = "dev-secret-key"
BASE_URL = "http://127.0.0.1:8000"


def sign_request(method: str, path: str, body: str = ""):
    """
    Creates a timestamp + HMAC SHA256 signature that matches your FastAPI server.
    """
    timestamp = str(int(time.time()))
    message = f"{timestamp}{method}{path}".encode() + body.encode()

    signature = hmac.new(
        API_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

    return timestamp, signature


def demo_get_prices():
    method = "GET"
    path = "/prices"
    body = ""  # GET requests have empty body

    timestamp, signature = sign_request(method, path, body)

    headers = {
        "X-Api-Key": API_KEY,
        "X-Timestamp": timestamp,
        "X-Signature": signature
    }

    print("Sending request...")
    response = requests.get(BASE_URL + path, headers=headers)

    print("Status:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except:
        print("No JSON returned.")

def demo_post_price():
    method = "POST"
    path = "/prices"

    payload = {
        "date": "2024-01-01",
        "price": 82.5
    }

    # Canonical JSON body (must match server exactly)
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)

    timestamp, signature = sign_request(method, path, body)

    headers = {
        "X-Api-Key": API_KEY,
        "X-Timestamp": timestamp,
        "X-Signature": signature,
        "Content-Type": "application/json"
    }

    print("Sending POST /prices ...")
    response = requests.post(BASE_URL + path, headers=headers, data=body)

    print("Status:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except:
        print("No JSON returned.")
        
if __name__ == "__main__":
    demo_post_price()
