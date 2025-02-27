import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor

def run_backend():
    """Run the FastAPI backend server."""
    os.chdir("backend")
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"])

def run_frontend():
    """Run the Streamlit frontend."""
    os.chdir("frontend")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "Home.py"])

def main():
    """Run both servers concurrently."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_backend)
        executor.submit(run_frontend)

if __name__ == "__main__":
    main() 