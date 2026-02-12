# SigNexus Setup (Digital Signature Demo)

This repo is a 3-layer demo. We keep everything consistent across teammates.

## Tech Stack (Required)
- Python 3.11+ (works on 3.13 too)
- FastAPI
- Uvicorn
- cryptography (Python lib)
- OpenSSL (CLI)

## Repo Structure (Target)
digital-signature-demo/
├─ receiver/                 # Level 3 (Verification backend - already implemented)
│  └─ app.py
├─ sender/                   # Level 1 (Signing service - teammate will implement)
├─ gateway/                  # Level 2 (Transmission/attack simulation - teammate will implement)
├─ public.pem                # Public key used by receiver to verify
├─ .gitignore
└─ README.md

> Note: sender/ and gateway/ are expected folders. Create them when you start your layer.

## Install Python deps
From repo root:
```bash
pip install fastapi uvicorn cryptography
