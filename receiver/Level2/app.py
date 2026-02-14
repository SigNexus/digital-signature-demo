from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib

app = FastAPI(title="Receiver (Level 2 - Hash Verification)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VerifyHashRequest(BaseModel):
    message: str
    hash: str

@app.get("/")
def health():
    return {"status": "receiver level 2 running", "endpoints": ["/verify"]}

@app.post("/verify")
def verify_hash(req: VerifyHashRequest):
    message_bytes = req.message.encode("utf-8")
    expected_hash = hashlib.sha256(message_bytes).hexdigest()
    
    if req.hash == expected_hash:
        return {"status": "Hash Valid ✅"}
    else:
        return {"status": "Hash Invalid ❌ (message tampered or wrong hash)"}
