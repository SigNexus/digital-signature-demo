from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import requests
import os

app = FastAPI(title="Sender (Level 2 - Hashing)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HashRequest(BaseModel):
    message: str

RECEIVER_URL = "http://127.0.0.1:8011/verify"

@app.on_event("startup")
def startup_event():
    proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    if proxy:
        print(f"DEBUG: Proxy detected - {proxy}")
        print("DEBUG: Outgoing requests will be intercepted by Burp Suite.")

@app.get("/")
def health():
    return {"status": "sender level 2 running", "endpoints": ["/hash", "/forward"]}

@app.post("/hash")
def hash_message(req: HashRequest):
    message_bytes = req.message.encode("utf-8")
    message_hash = hashlib.sha256(message_bytes).hexdigest()
    
    return {
        "message": req.message,
        "hash": message_hash
    }

@app.post("/forward")
def forward_message(req: HashRequest):
    # This endpoint is for Burp Suite demos.
    # It sends the message + hash directly to the receiver.
    message_bytes = req.message.encode("utf-8")
    message_hash = hashlib.sha256(message_bytes).hexdigest()
    
    payload = {
        "message": req.message,
        "hash": message_hash
    }
    
    try:
        response = requests.post(RECEIVER_URL, json=payload)
        return {
            "sender_sent": payload,
            "receiver_response": response.json()
        }
    except Exception as e:
        return {"error": f"Could not connect to Receiver: {str(e)}"}
