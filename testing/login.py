import time
import hmac
import hashlib
import requests
import json
import logging
from typing import Optional, Dict, Any

API_KEY = "dev-api-key"
API_SECRET = "dev-secret-key"
BASE_URL = "http://81.109.22.44:7578"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CLIENT] %(levelname)s: %(message)s"
)

class SecureAPIClient:
    def __init__(self, base_url=BASE_URL, api_key=API_KEY, api_secret=API_SECRET):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret

    def sign_request(self, method: str, path: str, body_bytes: bytes):
        timestamp = str(int(time.time()))

        # EXACT match to server logic
        message = f"{timestamp}{method}{path}".encode() + body_bytes

        signature = hmac.new(
            self.api_secret.encode(),
            message,
            hashlib.sha256
        ).hexdigest()

        return timestamp, signature

    def request(self, method: str, path: str, data: Optional[Dict] = None):
        # Raw body bytes (server uses raw bytes)
        body_bytes = b""
        if data is not None:
            body_bytes = json.dumps(data, separators=(", ", ": ")).encode()


        path_for_signing = path.split("?", 1)[0].rstrip("/")

        timestamp, signature = self.sign_request(method, path_for_signing, body_bytes)

        headers = {
            "X-Api-Key": self.api_key,
            "X-Timestamp": timestamp,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        url = self.base_url + path

        logging.info(f"{method} {url}")

        start = time.time()

        response = requests.request(
            method,
            url,
            headers=headers,
            data=body_bytes if method in ("POST", "PUT") else None
        )

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
