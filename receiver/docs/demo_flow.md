
---

## ✅ `receiver/docs/demo_flow.md` (copy/paste)

```md
# SigNexus Demo Flow (3 Layers)

Goal: show why digital signatures guarantee:
1) Integrity
2) Authentication
3) Non-repudiation

We demonstrate success + failure (tampering).

---

## What Each Layer Does

### Level 1 — Sender (Signing)
Responsible for:
- Accept a message string
- Produce a digital signature using private key
- Output:
  - message
  - signature_b64 (base64 one-line)

Expected endpoints (recommended):
- GET /health
- POST /sign
  Body:
  {
    "message": "Pay $1000 to Ali"
  }
  Response:
  {
    "message": "...",
    "signature_b64": "..."
  }

Notes:
- Signing must use SHA-256 and RSA.
- Output signature must be base64 ONE LINE (no newlines).

---

### Level 2 — Gateway (Transmission + Attack Simulation)
Responsible for:
- Receive (message + signature)
- Forward to receiver /verify
- Demonstrate attacker changing message in transit

Modes (recommended):
- mode=pass  → forward as-is (should verify ✅)
- mode=tamper → modify message (must fail ❌)

Expected endpoint (recommended):
- POST /forward?mode=pass|tamper
  Body:
  {
    "message": "...",
    "signature_b64": "..."
  }
  Response:
  {
    "forwarded_message": "...",
    "receiver_result": { ... }
  }

Tamper example:
- "Pay $1000 to Ali" → "Pay $9000 to Ali"
- Keep signature unchanged (this is the key point)

---

### Level 3 — Receiver (Verification) ✅ Already Implemented
Endpoint:
- POST /verify
  Body:
  {
    "message": "...",
    "signature_b64": "..."
  }

Output:
- "Signature Valid ✅"
- "Signature Invalid ❌ (message changed or wrong key)"

Receiver uses `public.pem` to verify.

---

## The 60–90 Second Live Demo Script (Recommended)

### Step A — Good Case (Valid)
1) Sender signs message:
   "Pay $1000 to Ali"
2) Gateway forwards without tampering
3) Receiver returns: ✅ Signature Valid

What to say:
- "Receiver verifies that the signature matches this exact message using the sender's public key."

### Step B — Attack Case (Tampered)
1) Use same signature
2) Gateway modifies message in transit:
   "Pay $9000 to Ali"
3) Receiver returns: ❌ Signature Invalid

What to say:
- "Even one-character change breaks verification."
- "This proves integrity + authentication. If it verifies, the sender must have had the private key."

---

## Demo Consistency Requirements (Team)
- Use the SAME message string exactly (spaces matter)
- Base64 signature must be one-line text
- Keep ports consistent:
  - sender: 8002
  - gateway: 8003
  - receiver: 8001

---

## Quick Verification Checklist
✅ Valid case works end-to-end  
✅ Tampered message fails verification  
✅ No private key committed to GitHub  
✅ Swagger UIs open for each service  
