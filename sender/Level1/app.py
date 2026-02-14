from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Sender (Level 1 - Plaintext)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

RECEIVER_URL = "http://127.0.0.1:8021/receive"

@app.on_event("startup")
def startup_event():
    proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    if proxy:
        print(f"DEBUG: Proxy detected - {proxy}")
        print("DEBUG: Outgoing requests will be intercepted by Burp Suite.")

@app.get("/")
def health():
    return {"status": "sender level 1 running", "endpoints": ["/send", "/forward"]}

@app.post("/send")
def send_message(req: MessageRequest):
    return {
        "message": req.message
    }

@app.post("/forward")
def forward_message(req: MessageRequest):
    # This endpoint is for Burp Suite demos. 
    # It sends the message directly to the receiver.
    payload = {"message": req.message}
    try:
        response = requests.post(RECEIVER_URL, json=payload)
        return {
            "sender_sent": payload,
            "receiver_response": response.json()
        }
    except Exception as e:
        return {"error": f"Could not connect to Receiver: {str(e)}"}
