from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

app = FastAPI(title="Receiver (Level 3 - Digital Signature Verification)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the sender's public key (shared)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "public.pem")

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = load_pem_public_key(f.read())

class VerifyRequest(BaseModel):
    message: str
    signature_b64: str  # signature encoded as base64 text

@app.get("/")
def health():
    return {"status": "receiver running", "endpoints": ["/verify"]}

@app.post("/verify")
def verify(req: VerifyRequest):
    print(f"DEBUG: Receiver Level 3 - Incoming Message: '{req.message}'")
    print(f"DEBUG: Receiver Level 3 - Incoming Signature (truncated): {req.signature_b64[:20]}...")
    try:
        signature = base64.b64decode(req.signature_b64)

        PUBLIC_KEY.verify(
            signature,
            req.message.encode("utf-8"),
            asy_padding.PKCS1v15(),
            hashes.SHA256(),
        )

        print("DEBUG: Receiver Level 3 - VERIFICATION SUCCESS")
        return {"status": "Signature Valid ✅"}

    except Exception as e:
        print(f"DEBUG: Receiver Level 3 - VERIFICATION FAILURE: {str(e)}")
        return {"status": "Signature Invalid ❌ (message changed or wrong key)"}
