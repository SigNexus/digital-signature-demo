import hashlib

def generate_hash():
    print("--- Level 2 Hashing Tool ---")
    print("Type a message to generate its SHA-256 hash.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        try:
            # 1. Get word/message from user input
            message = input("Enter message: ")
            
            if message.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
                
            # 2. Convert string to bytes
            message_bytes = message.encode("utf-8")
            
            # 3. Generate SHA-256 hash
            message_hash = hashlib.sha256(message_bytes).hexdigest()
            
            # 4. Output the exact hash expected by Level 2
            print(f"Generated Hash: {message_hash}\n")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error generating hash: {e}")

if __name__ == "__main__":
    generate_hash()
