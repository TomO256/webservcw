import time
import hmac
import hashlib
import requests
import json
import logging
from typing import Optional, Dict, Any

API_KEY = "dev-api-key"
API_SECRET = "dev-secret-key"
BASE_URL = "http://127.0.0.1:8000"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CLIENT] %(levelname)s: %(message)s"
)

class SecureAPIClient:
    def __init__(self, base_url=BASE_URL, api_key=API_KEY, api_secret=API_SECRET):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret

    def sign_request(self, method: str, path: str, body: str = ""):
        timestamp = str(int(time.time()))
        message = f"{timestamp}{method}{path}".encode() + body.encode()
        signature = hmac.new(
            self.api_secret.encode(),
            message,
            hashlib.sha256
        ).hexdigest()
        return timestamp, signature

    def request(self, method: str, path: str, data: Optional[Dict] = None):
        body = (
            json.dumps(data, separators=(",", ":"), sort_keys=True)
            if data else ""
        )

        # Normalize path for signing
        path_for_signing = path.split("?", 1)[0].rstrip("/")

        timestamp, signature = self.sign_request(method, path_for_signing, body)

        headers = {
            "X-Api-Key": self.api_key,
            "X-Timestamp": timestamp,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        url = self.base_url + path

        logging.info(f"{method} {url}")

        start = time.time()

        if method in ("GET", "DELETE"):
            response = requests.request(method, url, headers=headers)
        else:
            response = requests.request(method, url, headers=headers, data=body)

        duration = (time.time() - start) * 1000
        logging.info(f"Response {response.status_code} in {duration:.2f}ms")

        try:
            return response, response.json()
        except:
            return response, None

    def get(self, path: str):
        return self.request("GET", path)

    def post(self, path: str, data: dict):
        return self.request("POST", path, data)

    def put(self, path: str, data: Dict[str, Any]):
        return self.request("PUT", path, data)

    def delete(self, path: str):
        return self.request("DELETE", path)


if __name__ == "__main__":
    client = SecureAPIClient()
    response, data = client.get("/prices")
    print(data)
