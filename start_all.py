import subprocess
import time
import os
import sys

# Define services with their ports and module paths
# We consolidated all 6 individual sender/receiver pairs into a single app
# running on port 8000.

# Path to python in venv
if sys.platform == "win32":
    python_exe = os.path.join("venv", "Scripts", "python.exe")
else:
    python_exe = os.path.join("venv", "bin", "python")

uvicorn_exe = os.path.join(os.path.dirname(python_exe), "uvicorn")
process = None

try:
    print("--- Starting Unified Quantum Vault Server ---")
    print("Starting all backend and frontend services on port 8000...")
    process = subprocess.Popen(
        [uvicorn_exe, "app:app", "--port", "8000", "--host", "127.0.0.1", "--reload"]
    )

    print("\nAll systems online!")
    print("Web UI / Frontend: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server.")

    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down server...")
    if process:
        process.terminate()
    print("Stopped.")
except Exception as e:
    print(f"\nError: {e}")
    if process:
        process.terminate()
