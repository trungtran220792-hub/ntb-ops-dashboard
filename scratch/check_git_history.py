import subprocess
import sys

def check_history():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 1. Commit Log
    print("=== GIT COMMIT LOG ===")
    try:
        out = subprocess.check_output(
            ["git", "log", "-n", "15", "--pretty=format:%h - %ad - %s", "--date=format:%Y-%m-%d %H:%M:%S"],
            encoding='utf-8', errors='ignore'
        )
        print(out)
    except Exception as e:
        print("Error getting log:", e)
        
    # 2. Stash List
    print("\n=== GIT STASH LIST ===")
    try:
        out = subprocess.check_output(["git", "stash", "list"], encoding='utf-8', errors='ignore')
        print(out if out.strip() else "No stashes found.")
    except Exception as e:
        print("Error getting stash:", e)
        
    # 3. Branches
    print("\n=== GIT BRANCHES ===")
    try:
        out = subprocess.check_output(["git", "branch", "-a"], encoding='utf-8', errors='ignore')
        print(out)
    except Exception as e:
        print("Error getting branch:", e)

    # 4. Reflog (to see if there were hard resets or deleted branches)
    print("\n=== GIT REFLOG ===")
    try:
        out = subprocess.check_output(
            ["git", "reflog", "-n", "20", "--date=iso"],
            encoding='utf-8', errors='ignore'
        )
        print(out)
    except Exception as e:
        print("Error getting reflog:", e)

if __name__ == "__main__":
    check_history()
