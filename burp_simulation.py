import requests
import json
import sys
import base64
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding

# Ensure UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

BASE_SENDER = "http://127.0.0.1:8000/level"
BASE_RECEIVER = "http://127.0.0.1:8000/level"

def print_result(level, test_name, expected, actual, details=""):
    status = "PASS" if expected == actual else "FAIL"
    print(f"[{status}] {level} - {test_name}")
    if status == "FAIL":
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")
    if details:
        print(f"  Details:  {details}")

def test_level1_burp():
    print("\n--- Level 1: Plaintext (Burp Simulation) ---")
    # Scenario: Intercept -> Modify -> Forward
    msg = "Pay $1000 to Ali"
    tampered_msg = "Pay $9000 to Ali"
    
    print(f"1. Original Message: '{msg}'")
    print(f"2. Attacker Intercepts & Modifies to: '{tampered_msg}'")
    
    # Simulate forwarding tampered message to Receiver
    url = f"{BASE_RECEIVER}1/receive"
    payload = {"message": tampered_msg}
    
    try:
        res = requests.post(url, json=payload, timeout=5)
        data = res.json()
        print(f"3. Receiver Response: {data}")
        
        # In Level 1, there is NO check, so it should just accept it.
        # This PROVES the vulnerability.
        accepted = "Message Received (No Security)" in data.get("status", "")
        print_result("Level 1", "Tamper Vulnerability Check", True, accepted, "Receiver accepted tampered message (VULNERABLE as expected)")
    except Exception as e:
        print(f"ERROR: {e}")

def test_level2_burp():
    print("\n--- Level 2: Hashing (Burp Simulation) ---")
    # Scenario: Intercept -> Modify Message -> Keep Original Hash -> Forward
    msg = "Pay $1000 to Ali"
    tampered_msg = "Pay $9000 to Ali"
    
    # 1. Get valid hash for original message
    original_hash = hashlib.sha256(msg.encode()).hexdigest()
    print(f"1. Original Message: '{msg}'")
    print(f"2. Original Hash: {original_hash[:10]}...")
    
    # 2. Attacker modifies message but CANNOT easily forgery a valid hash for new message without being noticed?
    # Actually, hashing alone doesn't prove WHO sent it, but if we change message and keep old hash, it fails integrity.
    print(f"3. Attacker modifies message to '{tampered_msg}' but keeps OLD hash.")
    
    url = f"{BASE_RECEIVER}2/verify"
    payload = {
        "message": tampered_msg,
        "hash": original_hash
    }
    
    try:
        res = requests.post(url, json=payload, timeout=5)
        data = res.json()
        print(f"4. Receiver Response: {data}")
        
        # Should fail
        rejected = "Hash Mismatch" in data.get("status", "") or "Invalid" in data.get("status", "")
        print_result("Level 2", "Tamper Detection", True, rejected, "Receiver rejected tampered message (SECURE Integrity)")
    except Exception as e:
        print(f"ERROR: {e}")

def test_level3_burp():
    print("\n--- Level 3: Digital Signature (Burp Simulation) ---")
    # Scenario: Intercept -> Modify Message -> Keep Original Signature -> Forward
    msg = "Pay $1000 to Ali"
    tampered_msg = "Pay $9000 to Ali"
    
    # 1. Sign original message (using Sender's key)
    # We can use the sender app to get a valid signature first
    sender_res = requests.post(f"{BASE_SENDER}3/sign", json={"message": msg}).json()
    valid_sig = sender_res["signature_b64"]
    
    print(f"1. Original Message: '{msg}'")
    print(f"2. Valid Signature: {valid_sig[:10]}...")
    
    # 3. Attacker modifies message
    print(f"3. Attacker modifies message to '{tampered_msg}' but keeps OLD signature.")
    
    url = f"{BASE_RECEIVER}3/verify"
    payload = {
        "message": tampered_msg,
        "signature_b64": valid_sig
    }
    
    try:
        res = requests.post(url, json=payload, timeout=5)
        data = res.json()
        print(f"4. Receiver Response: {data}")
        
        # Should fail
        rejected = "Invalid" in data.get("status", "")
        print_result("Level 3", "Tamper Detection", True, rejected, "Receiver rejected tampered message (SECURE Auth+Integrity)")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    print("=== STARTING SECURITY SIMULATION (BURP SUITE STYLE) ===")
    test_level1_burp()
    test_level2_burp()
    test_level3_burp()
    print("\n=== SIMULATION COMPLETE ===")
