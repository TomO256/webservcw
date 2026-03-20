# Oil Price and Geopolitical Events  API

A FastAPI backend for managing oil prices and geopolitical events.

The API Documentation can be found in `API Docs.pdf`

## Main Folders

src/  
Contains the full FastAPI backend, including models, schemas, CRUD logic, database session management, and the main application entrypoint.

testing/  
Contains Python scripts that test individual API components such as authentication, analytics, events, and CRUD operations.

## Directory Structure

src/  
 ├── __init__.py  
 ├── crud.py  
 ├── db.py  
 ├── getData.py  
 ├── main.py  
 ├── models.py  
 ├── schemas.py  
 └── __pycache__/  
testing/  
 ├── analytics.py  
 ├── events.py  
 ├── login.py  
 ├── prices.py  
 ├── security.py  
 └── __pycache__/  
.gitignore  
API Docs.pdf  
demo.py  
oil.db  
README.md  
requirements.txt  
run_tests.py  

## Setup and Installation

1. Clone the repo
`git clone https://github.com/TomO256/webservcw.git`   
`cd webservcw`  
2. Create Virtual Env
`python3 -m venv venv`  
`source venv/bin/activate`  
`pip install -r requirements.txt`  
3. Configure and Set API Keys
Recommend keeping as default for demonstration purposes  
`export API_KEY="dev-api-key"`  
`export API_SECRET="dev-secret-key"`  
4. Run the server
NOTE: The server is already running on 81.109.22.44:7578 - recommend using a simple client to connect to it  
`uvicorn src.main:app --host 0.0.0.0 --port 7578`  

For testing, execute: `python run_test.py`  

## Security 
This API uses HMAC Signing, the X-Timestamp (current UNIX Timestamp) and X-Signature must be given  
This format is:  
`timestamp + method + path + body`  
EG: `1700000000GET/prices{"price":82.5,"date":"2024-01-01"}`  
A signature is of the format: `hex(hmac_sha256(API_SECRET, message))` which must match the server's set key.  
For 81.109.22.44:7578, the demonstration key is `'dev-secret-key'`  

## Example cURL
`curl -X GET "http://81.109.22.44:7578/prices" -H "X-Api-Key: your-key" -H "X-Timestamp: $(date +%s)" -H "X-Signature: <computed-signature>"`
