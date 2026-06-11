import subprocess

def run_cmd(args):
    res = subprocess.run(args, capture_output=True, text=True)
    return res.stdout.strip()

print("Searching for renderNtbAnalysisTable in Git commits:")
out = run_cmd(["git", "log", "-S", "renderNtbAnalysisTable", "--oneline"])
print(out if out else "No commits found introducing/deleting renderNtbAnalysisTable.")

print("\nSearching for setAmOprSort in Git commits:")
out = run_cmd(["git", "log", "-S", "setAmOprSort", "--oneline"])
print(out if out else "No commits found introducing/deleting setAmOprSort.")
