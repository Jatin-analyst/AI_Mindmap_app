"""
Script to run the Streamlit frontend.
"""
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = os.getenv("STREAMLIT_SERVER_PORT", "8501")
    
    print(f"Starting Streamlit frontend on port {port}")
    print(f"Frontend available at http://localhost:{port}")
    
    subprocess.run([
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.port",
        port
    ])
