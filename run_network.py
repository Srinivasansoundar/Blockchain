import subprocess
import sys
import time
import signal
import os

def run_node(port):
    """Run a blockchain node on specified port"""
    cmd = [sys.executable, "main.py", "--port", str(port)]
    return subprocess.Popen(cmd)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down network...")
    for process in processes:
        process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    # Default ports for the network
    ports = [8000, 8001, 8002]
    processes = []
    
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 50)
    print("P2P Blockchain Network Launcher")
    print("=" * 50)
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("Error: main.py not found in current directory")
        sys.exit(1)
    
    # Check if templates directory exists
    if not os.path.exists("templates"):
        print("Error: templates directory not found")
        print("Please create the templates directory and add dashboard.html")
        sys.exit(1)
    
    print("Starting P2P Blockchain Network...")
    print("This will start 3 nodes on ports 8000, 8001, and 8002")
    print("Press Ctrl+C to stop all nodes")
    print("-" * 50)
    
    for port in ports:
        print(f"Starting node on port {port}...")
        try:
            process = run_node(port)
            processes.append(process)
            time.sleep(3)  # Give each node time to start
        except Exception as e:
            print(f"Failed to start node on port {port}: {e}")
    
    print("\nAll nodes started successfully!")
    print("Access the blockchain network at:")
    for port in ports:
        print(f"  Node {port-7999}: http://localhost:{port}")
    
    print("\nTo connect the nodes:")
    print("1. Open each URL in your browser")
    print("2. Register peers on each node:")
    print("   - On Node 1 (8000): Add localhost:8001 and localhost:8002")
    print("   - On Node 2 (8001): Add localhost:8000 and localhost:8002")
    print("   - On Node 3 (8002): Add localhost:8000 and localhost:8001")
    print("3. Start creating transactions and mining blocks!")
    
    try:
        # Wait for all processes
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)