from fastapi import FastAPI
from pydantic import BaseModel
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

app = FastAPI(title="Receiver (Level 3 - Digital Signature Verification)")

# Load the sender's public key (shared)
from pathlib import Path

PUBLIC_KEY_PATH = Path(__file__).parent / "public.pem"

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
    try:
        signature = base64.b64decode(req.signature_b64)

        PUBLIC_KEY.verify(
            signature,
            req.message.encode("utf-8"),
            asy_padding.PKCS1v15(),
            hashes.SHA256(),
        )

        return {"status": "Signature Valid ✅"}

    except Exception:
        return {"status": "Signature Invalid ❌ (message changed or wrong key)"}
