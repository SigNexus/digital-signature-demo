import requests
import time
import subprocess
import os

def test_level(level, sender_port, receiver_port, sender_path, receiver_path):
    print(f"\n--- Testing Level {level} ---")
    
    # Start processes
    sender_proc = subprocess.Popen(["uvicorn", f"sender.Level{level}.app:app", "--port", str(sender_port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    receiver_proc = subprocess.Popen(["uvicorn", f"receiver.Level{level}.app:app", "--port", str(receiver_port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(3) # Wait for startup
    
    try:
        # 1. Get payload from Sender
        message = "Test message for level " + str(level)
        if level == 1:
            res = requests.post(f"http://localhost:{sender_port}/send", json={"message": message})
            payload = res.json()
            # Forward to receiver
            res_rec = requests.post(f"http://localhost:{receiver_port}/receive", json=payload)
        elif level == 2:
            res = requests.post(f"http://localhost:{sender_port}/hash", json={"message": message})
            payload = res.json()
            # Forward to receiver
            res_rec = requests.post(f"http://localhost:{receiver_port}/verify", json=payload)
        elif level == 3:
            res = requests.post(f"http://localhost:{sender_port}/sign", json={"message": message})
            payload = res.json()
            # Forward to receiver
            res_rec = requests.post(f"http://localhost:{receiver_port}/verify", json=payload)
        
        print(f"Level {level} Result: {res_rec.json()}")
        
    finally:
        sender_proc.terminate()
        receiver_proc.terminate()

if __name__ == "__main__":
    test_level(1, 8003, 8004, "", "")
    test_level(2, 8005, 8006, "", "")
    test_level(3, 8007, 8008, "", "")
