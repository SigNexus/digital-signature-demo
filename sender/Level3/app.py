from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import os
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

app = FastAPI(title="Sender (Level 3 - Digital Signature Signing)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load private key
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "private.pem")

with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = load_pem_private_key(f.read(), password=None)

class SignRequest(BaseModel):
    message: str

RECEIVER_URL = "http://127.0.0.1:8001/verify"

@app.on_event("startup")
def startup_event():
    proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    if proxy:
        print(f"DEBUG: Proxy detected - {proxy}")
        print("DEBUG: Outgoing requests will be intercepted by Burp Suite.")

@app.get("/")
def health():
    return {"status": "sender level 3 running", "endpoints": ["/sign", "/forward"]}

@app.post("/sign")
def sign_message(req: SignRequest):
    message_bytes = req.message.encode("utf-8")
    
    signature = PRIVATE_KEY.sign(
        message_bytes,
        asy_padding.PKCS1v15(),
        hashes.SHA256(),
    )
    
    signature_b64 = base64.b64encode(signature).decode("utf-8")
    
    return {
        "message": req.message,
        "signature_b64": signature_b64
    }

@app.post("/forward")
def forward_message(req: SignRequest):
    message_bytes = req.message.encode("utf-8")
    
    signature = PRIVATE_KEY.sign(
        message_bytes,
        asy_padding.PKCS1v15(),
        hashes.SHA256(),
    )
    
    signature_b64 = base64.b64encode(signature).decode("utf-8")
    
    payload = {
        "message": req.message,
        "signature_b64": signature_b64
    }
    
    # Force proxy use if set in environment
    proxy_url = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    
    if proxies:
        print(f"DEBUG: Forwarding through proxy {proxy_url}")

    try:
        # We use timeout and explicit proxies to ensure Burp compatibility
        response = requests.post(RECEIVER_URL, json=payload, proxies=proxies, timeout=10)
        return {
            "sender_sent": payload,
            "receiver_response": response.json()
        }
    except Exception as e:
        return {"error": f"Could not connect to Receiver: {str(e)}"}
