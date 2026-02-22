from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import hashlib
import requests
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from fastapi.responses import FileResponse

# Initialize single unified generic app
app = FastAPI(title="Quantum Vault: MEGA EDITION API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# -----------------
# Pydantic Models
# -----------------
class MessageRequest(BaseModel):
    message: str

class HashRequest(BaseModel):
    message: str

class VerifyHashRequest(BaseModel):
    message: str
    hash: str

class SignRequest(BaseModel):
    message: str

class VerifySignatureRequest(BaseModel):
    message: str
    signature_b64: str


# -----------------
# Cryptography Keys Setup
# -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "private.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "public.pem")

try:
    with open(PRIVATE_KEY_PATH, "rb") as f:
        PRIVATE_KEY = load_pem_private_key(f.read(), password=None)
    with open(PUBLIC_KEY_PATH, "rb") as f:
        PUBLIC_KEY = load_pem_public_key(f.read())
except Exception as e:
    print(f"WARNING: Could not load RSA keys. Level 3 will fail. Run generate_keys.py first. Error: {e}")
    PRIVATE_KEY = None
    PUBLIC_KEY = None


# -----------------
# LEVEL 1: Plaintext
# -----------------
level1_router = APIRouter(prefix="/level1", tags=["Level 1 - Plaintext"])

@level1_router.post("/send")
def l1_send(req: MessageRequest):
    return {"message": req.message}

@level1_router.post("/receive")
def l1_receive(req: MessageRequest):
    return {
        "status": "Message Received (No Security) ✅",
        "message": req.message
    }


# -----------------
# LEVEL 2: Hashing
# -----------------
level2_router = APIRouter(prefix="/level2", tags=["Level 2 - Hashing"])

@level2_router.post("/hash")
def l2_hash(req: HashRequest):
    message_bytes = req.message.encode("utf-8")
    message_hash = hashlib.sha256(message_bytes).hexdigest()
    return {
        "message": req.message,
        "hash": message_hash
    }

@level2_router.post("/verify")
def l2_verify(req: VerifyHashRequest):
    message_bytes = req.message.encode("utf-8")
    expected_hash = hashlib.sha256(message_bytes).hexdigest()
    
    if req.hash == expected_hash:
        return {"status": "Hash Valid ✅", "message": req.message}
    else:
        return {"status": "Hash Invalid ❌ (message tampered or wrong hash)"}


# -----------------
# LEVEL 3: Digital Signatures
# -----------------
level3_router = APIRouter(prefix="/level3", tags=["Level 3 - Signatures"])

@level3_router.post("/sign")
def l3_sign(req: SignRequest):
    if not PRIVATE_KEY:
        return {"error": "Private key not loaded"}
        
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

@level3_router.post("/verify")
def l3_verify(req: VerifySignatureRequest):
    if not PUBLIC_KEY:
        return {"error": "Public key not loaded"}
        
    print(f"DEBUG: Receiver Level 3 - Incoming Message: '{req.message}'")
    try:
        signature = base64.b64decode(req.signature_b64)
        PUBLIC_KEY.verify(
            signature,
            req.message.encode("utf-8"),
            asy_padding.PKCS1v15(),
            hashes.SHA256(),
        )
        print("DEBUG: Receiver Level 3 - VERIFICATION SUCCESS")
        return {"status": "Signature Valid ✅", "message": req.message}
    except Exception as e:
        print(f"DEBUG: Receiver Level 3 - VERIFICATION FAILURE: {str(e)}")
        return {"status": "Signature Invalid ❌ (message changed or wrong key)"}


# -----------------
# Include Routers
# -----------------
app.include_router(level1_router)
app.include_router(level2_router)
app.include_router(level3_router)

# -----------------
# Frontend Serving
# -----------------
@app.get("/")
def serve_frontend():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(
            index_path, 
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    return {"error": "index.html not found in root directory."}

if __name__ == "__main__":
    import uvicorn
    # When run directly, start the unified server
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
