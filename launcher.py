import subprocess
import sys
import os
import webbrowser
import time
import signal
import atexit
import psutil
import win32process
import win32con

def run_frontend():
    os.chdir('Frontend')
    frontend_process = subprocess.Popen(['npm', 'run', 'dev'], 
                                      shell=True,
                                      creationflags=subprocess.CREATE_NEW_CONSOLE | win32con.CREATE_NEW_PROCESS_GROUP)
    return frontend_process

def run_backend():
    os.chdir('Backend')
    backend_process = subprocess.Popen([sys.executable, 'app.py'],
                                     shell=True,
                                     creationflags=subprocess.CREATE_NEW_CONSOLE | win32con.CREATE_NEW_PROCESS_GROUP)
    return backend_process

def cleanup(processes):
    for process in processes:
        try:
            # Get the process ID
            pid = process.pid
            
            # Get all child processes
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            # Terminate all child processes
            for child in children:
                try:
                    child.terminate()
                except:
                    pass
            
            # Terminate the main process
            process.terminate()
            
            # Force kill if still running
            try:
                process.wait(timeout=3)
            except:
                process.kill()
        except:
            pass

def main():
    # Display startup message
    print("\n🚀 BoardCast")
    print("=" * 50)
    cpu_cores = os.cpu_count() or 4
    print(f"💻 System: {cpu_cores} CPU cores detected")
    print("🌐 Starting server...")
    print("=" * 50 + "\n")
    
    # Store original directory
    original_dir = os.getcwd()
    
    # Start frontend
    frontend_process = run_frontend()
    
    # Wait a bit for frontend to start
    
    # Go back to original directory
    os.chdir(original_dir)
    
    # Start backend
    backend_process = run_backend()
    
    # Store processes for cleanup
    processes = [frontend_process, backend_process]
    atexit.register(cleanup, processes)
    
    # Open browser after a short delay
    webbrowser.open('http://localhost:5173')
    
    print("Application Working!")
    print("Press Ctrl+C to stop all server.")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        cleanup(processes)

if __name__ == "__main__":
    main() 