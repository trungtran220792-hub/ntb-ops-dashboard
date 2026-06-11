# -*- coding: utf-8 -*-
import subprocess
import os
import signal
import time

def restart():
    print("Searching for python processes running app.py...")
    # We can use wmic on Windows to get command line arguments of processes
    try:
        cmd = 'wmic process where "name=\'python.exe\'" get ProcessId,CommandLine'
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        lines = res.stdout.splitlines()
        
        target_pid = None
        for line in lines:
            if "app.py" in line and "restart_server.py" not in line:
                parts = line.strip().split()
                if parts:
                    pid = parts[-1]
                    try:
                        target_pid = int(pid)
                        print(f"Found target process app.py with PID {target_pid}")
                        break
                    except ValueError:
                        pass
        
        if target_pid:
            print(f"Killing process {target_pid}...")
            os.kill(target_pid, signal.SIGTERM)
            time.sleep(2)
            # Check if still running, force kill if necessary
            try:
                os.kill(target_pid, 0)
                print("Process still alive, force killing...")
                os.kill(target_pid, signal.SIGABRT)
            except OSError:
                print("Process successfully killed.")
        else:
            print("No running app.py process found.")
            
    except Exception as e:
        print(f"Error finding/killing process: {e}")

if __name__ == "__main__":
    restart()
