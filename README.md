# Oil Price and Geopolitical Events  API

This project is an Application Program Interface (API) for collecting and analysing datasets related to the price of oil, and its relevance during major geopolitical events. It uses a RESTful architecture which is hosted on a public server, created specifically for this coursework, written in Python, with a FastAPI and SQL backend database. The aim is to allow a single API for both the collection of oil price statistics and geopolitical events to be easily accessible, allowing users to have one location in which they can query both these sets of data, for specific ranges, with specific filters, as well as updating these datapoints when necessary, with all CRUD actions implemented

The API Documentation can be found in `docs/API Docs.pdf` and at https://81.109.22.44:7578/docs

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
docs/  
 ├── API Docs.pdf   
 ├── Presentation.pptx   
 └── report.pdf  
.gitignore   
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
