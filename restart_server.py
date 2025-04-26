"""
Restart server script to apply API documentation changes
"""
import os
import sys
import signal
import subprocess
import time
import psutil

def find_process_by_port(port):
    """Find and return process using the given port"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            if proc.info['connections']:
                for conn in proc.info['connections']:
                    if conn.laddr.port == port and conn.status == 'LISTEN':
                        return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    process = find_process_by_port(port)
    if process:
        print(f"Killing process {process.info['pid']} ({process.info['name']}) on port {port}")
        try:
            # On Windows
            if os.name == 'nt':
                subprocess.run(['taskkill', '/F', '/PID', str(process.info['pid'])], 
                              check=True, capture_output=True)
            # On Unix-like systems
            else:
                os.kill(process.info['pid'], signal.SIGTERM)
            time.sleep(1)  # Give it some time to terminate
            return True
        except (subprocess.SubprocessError, OSError) as e:
            print(f"Error killing process: {e}")
            return False
    print(f"No process found using port {port}")
    return True

def main():
    """Main function to restart the server"""
    port = 8000
    
    # Step 1: Kill any process on the port
    print(f"Looking for processes on port {port}...")
    if not kill_process_on_port(port):
        print("Failed to kill existing process. Please stop the server manually.")
        return
    
    # Step 2: Start the server
    print("\nStarting server...")
    try:
        server_process = subprocess.Popen([sys.executable, "run.py"])
        print(f"Server started with PID {server_process.pid}")
        
        # Step 3: Wait for server to start
        print("Waiting for server to initialize...")
        time.sleep(5)
        
        # Step 4: Run the test script
        print("\nRunning test script for API documentation...")
        test_process = subprocess.run([sys.executable, "test_api_docs.py"], 
                                     check=True, capture_output=True, text=True)
        print(test_process.stdout)
        
        if test_process.returncode != 0:
            print(f"Test failed with exit code {test_process.returncode}")
            print(test_process.stderr)
        
        print("\nServer is running. Press Ctrl+C to stop.")
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
            server_process.terminate()
            server_process.wait(timeout=5)
            print("Server stopped.")
    
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main() 