import time
import hmac
import hashlib
import requests
from . import login

client = login.SecureAPIClient()

BASE = "http://127.0.0.1:8000"

def test_invalid_api_key():
    headers = {
        "X-API-Key": "wrong",
        "X-Timestamp": str(int(time.time())),
        "X-Signature": "abc"
    }
    r = requests.get(BASE + "/prices", headers=headers)
    assert r.status_code == 401

def test_expired_timestamp():
    ts = str(int(time.time()) - 999)
    sig = hmac.new(
        client.api_secret.encode(),
        f"{ts}GET/prices".encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "X-API-Key": client.api_key,
        "X-Timestamp": ts,
        "X-Signature": sig
    }
    r = requests.get(BASE + "/prices", headers=headers)
    assert r.status_code == 401

def test_invalid_signature():
    headers = {
        "X-API-Key": client.api_key,
        "X-Timestamp": str(int(time.time())),
        "X-Signature": "invalid"
    }
    r = requests.get(BASE + "/prices", headers=headers)
    assert r.status_code == 401
