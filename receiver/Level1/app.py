from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Receiver (Level 1 - Plaintext)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def health():
    return {"status": "receiver level 1 running", "endpoints": ["/receive"]}

@app.post("/receive")
def receive_message(req: MessageRequest):
    return {
        "status": "Message Received (No Security) ✅",
        "message": req.message
    }
